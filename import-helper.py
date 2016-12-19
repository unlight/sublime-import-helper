import sublime
import sublime_plugin
import os
from .utils import *

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

PROJECT_NAME = 'import-helper'
# settings = sublime.load_settings('import-helper')

PROJECT_DIRECTORY = None

SOURCE_ROOT = None
IMPORT_NODES = []

def setup():
    window = sublime.active_window()
    project_file = window.project_file_name()
    if not bool(project_file):
        message = 'There is no project file, {0} will not work without project.'.format(PROJECT_NAME)
        debug(message, force=True)
        sublime.status_message(message)
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
    sublime.status_message('{0}: {1} imports found'.format(PROJECT_NAME, len(result)))
    global IMPORT_NODES
    IMPORT_NODES = result

def read_packages_callback(err, result):
    if not bool(err):
        debug('Read packages result', len(result))

# =============================================== Plugin Lifecycle

def plugin_loaded():
    print()
    debug("Plugin loaded", PROJECT_NAME)
    setup()

# =============================================== Command insert_import

class InsertImportCommand(sublime_plugin.TextCommand):
    """ Adds import of identifier near cursor """
    def run(self, edit, selected=None):
        view = self.view
        # TODO: Handle all selections.
        if (selected is None):
            selected_region = view.sel()[0]
            selected = view.substr(selected_region)
        if not bool(selected):
            cursor_region = view.expand_by_class(selected_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            selected = view.substr(cursor_region)
        debug("Selected", selected)
        items = []
        panel_items = []
        for item in IMPORT_NODES:
            if (item['name'] == selected):
                items.append(item)
                panel_item = get_panel_item(SOURCE_ROOT, item)
                panel_items.append(panel_item)
        if (len(panel_items) == 0):
            view.show_popup('No imports found for `<strong>{0}</strong>`'.format(selected))
            return
        window = view.window()
        if (len(panel_items) == 1):
            view.run_command('do_insert_import', {'item': items[0]})
            return

        def on_select(selected_index):
            debug('Selected index', selected_index)
            if (selected_index == -1): return
            selected_item = items[selected_index]
            debug('Selected item', selected_item)
            view.run_command('do_insert_import', {'item': selected_item})
        window.show_quick_panel(panel_items, on_select)

# =============================================== Command list_imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    """ Show all available imports """
    def run(self, edit):
        view = self.view
        window = view.window()
        items = [get_panel_item(SOURCE_ROOT, item) for item in IMPORT_NODES]

        def on_select(index):
            debug('Selected index', index)
            if (index == -1): return
            selected_item = IMPORT_NODES[index]
            debug('Selected item', selected_item)
            view.run_command('do_insert_import', {'item': selected_item})
        window.show_quick_panel(items, on_select)

# window.run_command('update_imports')
# sublime.active_window().run_command('update_imports', args={'a':'bar'})
class UpdateImportsCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()

# view.run_command('import_from_clipboard')
class ImportFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_import', args=({'selected': sublime.get_clipboard()}))

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
