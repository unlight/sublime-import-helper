import sublime
import sublime_plugin
import os
from .utils import *

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

PROJECT_NAME = "import-helper"
SETTINGS_FILE = PROJECT_NAME + ".sublime-settings"

PROJECT_DIRECTORY = None
settings = sublime.load_settings(SETTINGS_FILE)
# TODO: Load and get settings value = settings.get("name")

SOURCE_ROOT = None
IMPORT_NODES = []

def setup_callback(err, result):
    if (bool(err)):
        return
    debug("Setup result", "OK")
    window = sublime.active_window()
    project_file = window.project_file_name()
    if (bool(project_file) == False):
        message = 'There is no project file, {0} will not work without project.'.format(PROJECT_NAME)
        debug(message, force = True)
        status_message(message)
        return
    project_data = window.project_data()
    
    global PROJECT_DIRECTORY
    folder = project_data['folders'][0]
    # TODO: Other folders not handled.
    folder_path = os.path.join(os.path.dirname(project_file), folder['path'])
    PROJECT_DIRECTORY = os.path.normpath(folder_path)
    debug('PROJECT_DIRECTORY', PROJECT_DIRECTORY)
    
    global SOURCE_ROOT
    sourceRoot = project_data.get('sourceRoot')
    if not sourceRoot:
        sourceRoot = PROJECT_DIRECTORY
    folder_path = os.path.join(os.path.dirname(project_file), sourceRoot)
    SOURCE_ROOT = os.path.normpath(folder_path)
    debug('SOURCE_ROOT', SOURCE_ROOT)
    run_command_async('get_packages', {'projectDirectory': SOURCE_ROOT}, get_packages_callback)

def get_packages_callback(err, result):
    if err:
        return
    debug('Get packages result', len(result))
    global IMPORT_NODES
    IMPORT_NODES = result

def read_packages_callback(err, result):
    if (bool(err) == False):
        debug('Read packages result', len(result))

# =============================================== Plugin Lifecycle

def plugin_loaded():
    print()
    debug("Plugin loaded", PROJECT_NAME)
    exec_async(["node", SETUP_PATH], setup_callback)
    
# =============================================== Command insert_import_statement

class InsertImportStatementCommand(sublime_plugin.TextCommand):
    """ Adds import of identifier near cursor """
    def run(self, edit):
        view = self.view
        # TODO: Handle all selections.
        selected_region = view.sel()[0]
        selected_str = view.substr(selected_region)
        if (bool(selected_str) == False):
            cursor_region = view.expand_by_class(selected_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            selected_str = view.substr(cursor_region)
        debug("selected_str", selected_str)
        items = []
        panel_items = []
        for item in IMPORT_NODES:
            if (item['name'] == selected_str):
                items.append(item)
                panel_item = get_panel_item(SOURCE_ROOT, item)
                panel_items.append(panel_item)
        if (len(panel_items) == 0):
            view.show_popup("No imports found for `<strong>{0}</strong>`".format(selected_str))
            return
        window = view.window()
        if (len(panel_items) == 1):
            view.run_command('do_insert_import_statement', {'item': items[0]})
            return
        def on_select(selected_index):
            debug('Selected index', selected_index)
            if (selected_index == -1): return
            selected_item = items[selected_index]
            debug('Selected item', selected_item)
            view.run_command('do_insert_import_statement', {'item': selected_item})
        window.show_quick_panel(panel_items, on_select)

# TEST: connection Author Photo PhotoMetadata Date findFile
class DoInsertImportStatementCommand(sublime_plugin.TextCommand):
    def run(self, edit, item):
        if (item.get('module')):
            module_path = item['module']
        else:
            file_name = self.view.file_name()
            module_path = os.path.relpath(item['filepath'], os.path.dirname(file_name))
            module_path = unixify(module_path)
            if module_path[0] != ".":
                module_path = "./" + module_path
        if item['isDefault']:
            import_string = "import {0} from '{1}';\n"
        else:
            import_string = "import {{ {0} }} from '{1}';\n"
        import_string = import_string.format(item['name'], module_path)
        debug('Import string', import_string)
        pos = 0
        self.view.insert(edit, pos, import_string)

# =============================================== Command list_imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    """ Show all available imports """
    def run(self, edit):
        view = self.view;
        window = view.window()
        items = [get_panel_item(SOURCE_ROOT, item) for item in IMPORT_NODES]
        def on_select(index):
            debug('Selected index', index)
            if (index == -1): return
            selected_item = IMPORT_NODES[index]
            debug('Selected item', selected_item)
            view.run_command('do_insert_import_statement', {'item': selected_item})
        window.show_quick_panel(items, on_select)

# view.run_command('test')
# class TestCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         # pong = run_command('ping')
#         # debug('pong', pong)
#         def callback(err, result):
#             debug('err', err)
#             if (bool(err)): return
#             debug('result', result)
#         pong = run_command_async('ping',data=None, callback=callback)
#         # debug('pong', pong)
