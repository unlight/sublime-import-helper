import sublime
import sublime_plugin
import os

PROJECT_NAME = "Import Helper"
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
RUN_PATH = os.path.join(PACKAGE_PATH, "backend_run.js")
NODE_BIN = "node"
NODE_MODULES = []  # Collection of entries
SOURCE_MODULES = []
TYPESCRIPT_PATHS = []

from .library.utils import get_time
from .library.get_setting import get_setting
from .library.debug import debug
from .library.find_executable import find_executable
from .library.update_source_modules import update_source_modules
from .library.update_node_modules import update_node_modules
from .library.list_imports_command import list_imports_command
from .library.get_from_paths import get_from_paths
from .library.insert_import_command import insert_import_command
from .library.paste_import_command import paste_import_command
from .library.update_typescript_paths import update_typescript_paths
from .library.query_completions_modules import query_completions_modules


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
    update_source_modules(SOURCE_MODULES)
    update_node_modules(NODE_MODULES)
    update_typescript_paths(TYPESCRIPT_PATHS)


# window.run_command('update_source_modules')
class UpdateSourceModulesCommand(sublime_plugin.WindowCommand):
    def run(self):
        update_source_modules(SOURCE_MODULES)


# Command list_imports - Show all available imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        list_imports_command(
            view=self.view,
            entry_modules=SOURCE_MODULES + NODE_MODULES,
            typescript_paths=TYPESCRIPT_PATHS,
        )


class PasteImportCommand(sublime_plugin.TextCommand):
    def run(
        self, edit, item, typescript_paths=TYPESCRIPT_PATHS, test_selected_index=-1
    ):
        replace_content = paste_import_command(
            view=self.view,
            item=item,
            typescript_paths=typescript_paths,
            test_selected_index=test_selected_index,
        )
        if type(replace_content) == str:
            self.view.replace(
                edit, sublime.Region(0, self.view.size()), replace_content
            )


# Adds import of identifier near cursor (insert_import)
# view.run_command('insert_import', args=({'name': 'createName'}))
class InsertImportCommand(sublime_plugin.TextCommand):
    def run(self, edit, name=None, point=None, notify=True):
        insert_import_command(
            view=self.view,
            name=name,
            point=point,
            notify=notify,
            entry_modules=SOURCE_MODULES + NODE_MODULES,
            typescript_paths=TYPESCRIPT_PATHS,
        )


# window.run_command('initialize_setup')
# sublime.active_window().run_command('initialize_setup', args={'a':'bar'})
class InitializeSetupCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()


# view.run_command('import_from_clipboard')
class ImportFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        insert_import_command(
            view=self.view,
            name=sublime.get_clipboard(),
            notify=True,
            entry_modules=SOURCE_MODULES + NODE_MODULES,
            typescript_paths=TYPESCRIPT_PATHS,
        )


class ImportHelperEventListener(sublime_plugin.EventListener):
    def __init__(self):
        self.viewIds = []

    def on_new(self, view):
        self.viewIds.append(view.id())

    def on_post_save(self, view):
        if view.id() in self.viewIds:
            self.viewIds.remove(view.id())
            update_source_modules(SOURCE_MODULES)


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
                self.autocomplete_point,
                "source.ts, source.ts.unittest, source.tsx, source.js, source.jsx",
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
                prefix=prefix, source_modules=SOURCE_MODULES, node_modules=NODE_MODULES
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
