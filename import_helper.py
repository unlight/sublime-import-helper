import sublime
import sublime_plugin
import os
import concurrent.futures

PROJECT_NAME = "Import Helper"
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
RUN_PATH = os.path.join(PACKAGE_PATH, "backend_run.js")
NODE_BIN = "node"
DEBUG = True
NODE_MODULES = []  # Collection of entries
SOURCE_MODULES = []
TYPESCRIPT_PATHS = []

from .library.get_setting import get_setting
from .library.debug import debug
from .library.find_executable import find_executable
from .library.update_source_modules import update_source_modules
from .library.list_imports_command import list_imports_command
from .library.get_from_paths import get_from_paths


def plugin_loaded():
    print()
    debug("Plugin loaded", PROJECT_NAME)
    sublime.set_timeout(initialize, 0)
    sublime.set_timeout(setup, 0)


def initialize():
    global NODE_BIN
    if NODE_BIN == "node" or not bool(NODE_BIN):
        NODE_BIN = get_setting("node_bin", "")
        if not bool(NODE_BIN):
            NODE_BIN = find_executable("node")
        if not bool(NODE_BIN):
            NODE_BIN = "node"


def setup():
    project_file = sublime.active_window().project_file_name()
    if project_file is None:
        message = "There is no project file, {0} will not work without project.".format(
            PROJECT_NAME
        )
        debug(message, force=True)
        sublime.status_message(message)
        return
    update_source_modules()
    # update_node_modules()
    # update_typescript_paths()


# window.run_command('update_source_modules')
class UpdateSourceModulesCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_source_modules()


# Command list_imports - Show all available imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        list_imports_command(
            {
                "view": self.view,
                "entry_modules": SOURCE_MODULES + NODE_MODULES,
                "typescript_paths": TYPESCRIPT_PATHS,
            }
        )


# Command insert_import
class InsertImportCommand(sublime_plugin.TextCommand):
    # Adds import of identifier near cursor

    def run(self, edit, name=None, point=None, notify=True):
        if name is None:
            point_region = self.view.sel()[0]
            if point is not None:
                point_region = sublime.Region(point, point)
            name = self.view.substr(point_region).strip()
            if not name:
                cursor_region = self.view.expand_by_class(
                    point_region,
                    sublime.CLASS_WORD_START
                    | sublime.CLASS_LINE_START
                    | sublime.CLASS_PUNCTUATION_START
                    | sublime.CLASS_WORD_END
                    | sublime.CLASS_PUNCTUATION_END
                    | sublime.CLASS_LINE_END,
                )
                name = self.view.substr(cursor_region)
        name = re.sub(r"[^\w\-\@\/]", "", name)
        if not name:
            return
        debug("insert_import: trying to import", "`{0}`".format(name))
        import_root = get_import_root()
        match_items = []
        panel_items = []
        # Iterate through source modules + node modules
        for item in source_modules + node_modules:
            if item.get("name") == name:
                panel_item = get_panel_item(import_root, item)
                if panel_item is not None:
                    panel_items.append(panel_item)
                    match_items.append(item)
        if len(panel_items) == 0 and notify:
            self.view.show_popup(
                "No imports found for `<strong>{0}</strong>`".format(name)
            )
            return
        if len(panel_items) == 1:
            item = match_items[0]
            self.view.run_command(
                "paste_import", {"item": item, "typescript_paths": typescript_paths}
            )
            return
        on_done = on_done_func(match_items, self.on_select)
        self.view.window().show_quick_panel(panel_items, on_done)

    def on_select(self, selected_item):
        debug("insert_import: on_select", selected_item)
        self.view.run_command(
            "paste_import",
            {"item": selected_item, "typescript_paths": typescript_paths},
        )


# window.run_command('initialize_setup')
# sublime.active_window().run_command('initialize_setup', args={'a':'bar'})
class InitializeSetupCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()


# view.run_command('import_from_clipboard')
class ImportFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_import", args=({"name": sublime.get_clipboard()}))


class PasteImportCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)

    def run(self, edit, item, typescript_paths=[]):
        debug("paste_import: item", item)
        file_name = self.view.file_name() or "."
        from_paths = get_from_paths(item, file_name, typescript_paths)
        if len(from_paths) == 0:
            raise Exception("len from_paths must be not empty")
        if len(from_paths) > 1:
            choices = [{"item": item, "path": path} for path in from_paths]

            def on_select(selected):
                item = selected.get("item")
                item["module"] = selected.get("path")
                self.view.run_command(
                    "paste_import", {"item": item, "typescript_paths": []}
                )

            self.view.window().show_quick_panel(
                from_paths, on_done_func(choices, on_select)
            )
            return
        # Get import line information
        from_path = from_paths[0]
        import_line_info = get_import_line_info(self.view, from_path)
        debug("paste_import: import_line_info", import_line_info)
        # Prepare import string template
        from_quote = get_setting("from_quote", "'")
        import_end = ";" if get_setting("from_semicolon", True) else ""
        import_string = "import {{0}} from {0}{2}{0}{1}\n".format(
            from_quote, import_end, from_path
        )
        # Name to import
        name = item["name"]
        if item.get("from_package") == True:
            name = identifier_name(name)
        # Not found in existing paths
        if import_line_info["import_row"] == -1:
            pos = 0
            if "end" == get_setting("insert_position", "end"):
                pos = self.view.text_point(import_line_info["last_import_row"] + 1, 0)
            if not item["isDefault"]:
                name = wrap_imports([name])
            self.view.insert(edit, pos, import_string.format(name))
            return
        # Import row found
        debug("import_line_info", import_line_info)
        line_region = self.view.full_line(
            self.view.text_point(import_line_info["import_row"], 0)
        )
        # Trying to import in import default row
        if (
            is_import_default(import_line_info["line_contents"])
            and item["isDefault"] == False
        ):
            name = import_line_info["imports"][0] + ", { " + name + " }"
            debug("name", name)
            self.view.replace(edit, line_region, import_string.format(name))
        # Trying to import non default item to mixed line
        elif (
            is_import_mixed(import_line_info["line_contents"])
            and item["isDefault"] == False
        ):
            other_imports = import_line_info["imports"][1:]
            try:
                other_imports.remove(name)
            except:
                pass
            other_imports.append(name)
            name = (
                import_line_info["imports"][0]
                + ", { "
                + ", ".join(other_imports)
                + " }"
            )
            debug("name", name)
            self.view.replace(edit, line_region, import_string.format(name))
        # Ttrying to import item default
        elif item["isDefault"]:
            if is_import_default(import_line_info["line_contents"]):
                name = "* as " + name
            debug("name", name)
            self.view.replace(edit, line_region, import_string.format(name))
        # Regular import
        else:
            imports = import_line_info["imports"]
            try:
                imports.remove(name)
            except:
                pass
            imports.append(name)
            line_region = self.view.full_line(
                self.view.text_point(import_line_info["import_row"], 0)
            )
            name = wrap_imports(imports)
            debug("name", name)
            self.view.replace(edit, line_region, import_string.format(name))


class ImportHelperEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.viewIds = []

    def on_new(self, view):
        self.viewIds.append(view.id())

    def on_post_save(self, view):
        if view.id() in self.viewIds:
            self.viewIds.remove(view.id())
            update_source_modules()


class ImportHelperViewEventListener(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        super().__init__(view)
        self.completions_info = {"time": -1, "result": [], "prefix": ""}
        self.in_auto_complete = False
        self.autocomplete_point = 0
        self.autocomplete_export_names = get_setting("autocomplete_export_names", True)
        self.autocomplete_auto_import = get_setting("autocomplete_auto_import", False)

    def on_query_completions(self, prefix, locations):
        if not self.autocomplete_export_names or not (
            len(prefix) > 0
            and self.view.match_selector(
                self.autocomplete_point, "source.ts, source.tsx, source.js, source.jsx"
            )
        ):
            return []
        self.autocomplete_point = locations[0]
        if (
            get_time() > self.completions_info["time"] + 1
            or prefix != self.completions_info["prefix"]
        ):
            self.completions_info["time"] = get_time()
            self.completions_info["prefix"] = prefix
            self.completions_info["result"] = query_completions_modules(
                prefix, SOURCE_MODULES, NODE_MODULES
            )
        return self.completions_info["result"]

    def on_post_text_command(self, command_name, args):
        if not (self.autocomplete_auto_import and self.autocomplete_export_names):
            return
        if self.in_auto_complete and command_name in [
            "insert_best_completion",
            "insert_dimensions",
        ]:
            self.in_auto_complete = False
            self.view.run_command(
                "insert_import",
                args=({"point": self.autocomplete_point - 1, "notify": False}),
            )
        elif command_name in [
            "auto_complete",
            "replace_completion_with_next_completion",
            "replace_completion_with_auto_complete",
        ]:
            self.in_auto_complete = True
        elif command_name == "hide_auto_complete":
            self.in_auto_complete = False

    def on_activated(self):
        self.in_auto_complete = False
