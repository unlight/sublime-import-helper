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


def plugin_loaded():
    print()
    debug("Plugin loaded", PROJECT_NAME)
    sublime.set_timeout(initialize, 0)
    # sublime.set_timeout(setup, 0)


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


# window.run_command('update_source_modules')
class UpdateSourceModulesCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_source_modules()


# view.run_command('import_from_clipboard')
class ImportFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("insert_import", args=({"name": sublime.get_clipboard()}))


# Command list_imports - Show all available imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        import_root = get_import_root()
        match_items = []
        panel_items = []
        for item in source_modules + node_modules:
            panel_item = get_panel_item(import_root, item)
            if panel_item is not None:
                panel_items.append(panel_item)
                match_items.append(item)
        on_done = on_done_func(match_items, self.on_select)
        self.view.window().show_quick_panel(panel_items, on_done)

    def on_select(self, selected_item):
        debug("list_imports:on_select", selected_item)
        self.view.run_command(
            "paste_import",
            {"item": selected_item, "typescript_paths": typescript_paths},
        )


class ImportHelperEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.viewIds = []

    def on_new(self, view):
        self.viewIds.append(view.id())

    def on_post_save(self, view):
        if view.id() in self.viewIds:
            self.viewIds.remove(view.id())
            update_source_modules()
