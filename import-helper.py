import sublime
import sublime_plugin
from .utils import *

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

PROJECT_NAME = 'Import Helper'
IMPORT_NODES = []

def setup():
    project_file = sublime.active_window().project_file_name()
    if not bool(project_file):
        message = 'There is no project file, {0} will not work without project.'.format(PROJECT_NAME)
        debug(message, force=True)
        sublime.status_message(message)
        return
    del IMPORT_NODES[:]
    import_root = get_import_root()
    source_folders = get_source_folders()
    debug('source_folders', source_folders)
    debug('import_root', import_root)
    run_command_async('get_packages', {'folders': source_folders}, get_packages_callback)
    run_command_async('get_packages', {'importRoot': import_root, 'packageKeys': ['dependencies']}, get_packages_callback)
    run_command_async('get_packages', {'importRoot': import_root, 'packageKeys': ['devDependencies']}, get_packages_callback)

def get_import_root():
    window = sublime.active_window()
    project_file = window.project_file_name()
    project_data = window.project_data()
    test_path = project_data.get('import_root')
    if bool(test_path):
        result = test_path
    else:
        result = project_data['folders'][0]['path']
    return norm_path(project_file, result)

def get_source_folders():
    window = sublime.active_window()
    project_file = window.project_file_name()
    project_data = window.project_data()
    result = []
    for folder in project_data['folders']:
        folder_path = folder['path']
        path_source = project_data.get('path_source')
        if bool(path_source):
            folder_path = path_source
        folder_path = norm_path(project_file, folder_path)
        result.append(folder_path)
    return result

def get_packages_callback(err, result):
    if err:
        sublime.error_message(PROJECT_NAME + '\n' + str(err))
        return
    IMPORT_NODES.extend(result)
    sublime.status_message('{0}: {1} imports found'.format(PROJECT_NAME, len(IMPORT_NODES)))
    debug('Get packages result', '{0} ({1})'.format(len(result), len(IMPORT_NODES)))

# =============================================== Plugin Lifecycle

def plugin_loaded():
    print()
    debug('Plugin loaded', PROJECT_NAME)
    setup()

# =============================================== Command insert_import

class InsertImportCommand(sublime_plugin.TextCommand):
    # Adds import of identifier near cursor
    def __init__(self, view):
        super().__init__(view)
        self.import_root = get_import_root()

    def run(self, edit, selected=None):
        view = self.view
        if (selected is None):
            selected_region = view.sel()[0]
            selected = view.substr(selected_region)
        if not bool(selected):
            cursor_region = view.expand_by_class(selected_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            selected = view.substr(cursor_region)
        debug('Selected', selected)
        items = []
        panel_items = []
        for item in IMPORT_NODES:
            if (item['name'] == selected):
                items.append(item)
                panel_item = get_panel_item(self.import_root, item)
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
    # Show all available imports
    def __init__(self, view):
        super().__init__(view)
        self.import_root = get_import_root()

    def run(self, edit):
        view = self.view
        window = view.window()
        items = [get_panel_item(self.import_root, item) for item in IMPORT_NODES]

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
