import sublime
import sublime_plugin
from .utils import *

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

PROJECT_NAME = 'Import Helper'
node_modules = []
source_modules = [];

def setup():
    project_file = sublime.active_window().project_file_name()
    if project_file is None:
        message = 'There is no project file, {0} will not work without project.'.format(PROJECT_NAME)
        debug(message, force=True)
        sublime.status_message(message)
        return
    update_source_modules()
    update_node_modules()

def update_source_modules():
    source_folders = get_source_folders()
    debug('source_folders', source_folders)
    def get_source_modules_callback(err, result):
        if err:
            sublime.error_message(PROJECT_NAME + '\n' + str(err))
            return
        source_modules.clear();
        source_modules.extend(result)
        sublime.status_message('{0}: {1} source modules found'.format(PROJECT_NAME, len(source_modules)))
        debug('Update source modules', len(source_modules))
    run_command_async('get_packages', {'folders': source_folders}, get_source_modules_callback)

def update_node_modules():
    node_modules.clear()
    import_root = get_import_root()
    debug('import_root', import_root)
    run_command_async('get_packages', {'importRoot': import_root, 'packageKeys': ['dependencies']}, get_packages_callback)
    run_command_async('get_packages', {'importRoot': import_root, 'packageKeys': ['devDependencies']}, get_packages_callback)    

def get_import_root():
    window = sublime.active_window()
    project_file = window.project_file_name()
    if project_file is None:
	    return
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
    node_modules.extend(result)
    sublime.status_message('{0}: {1} node modules found'.format(PROJECT_NAME, len(node_modules)))
    debug('Get packages result', len(result))

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
        if (selected is None):
            selected_region = self.view.sel()[0]
            selected = self.view.substr(selected_region)
        if not bool(selected):
            cursor_region = self.view.expand_by_class(selected_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            selected = self.view.substr(cursor_region)
        debug('Selected word region', selected)
        match_items = []
        panel_items = []
        # Iterate through source modules
        for item in source_modules:
            if (item['name'] == selected):
                match_items.append(item)
                panel_items.append(get_panel_item(self.import_root, item))            
        # Iterate through node modules
        for item in node_modules:
            if (item['name'] == selected):
                match_items.append(item)
                panel_items.append(get_panel_item(self.import_root, item))
        if (len(panel_items) == 0):
            self.view.show_popup('No imports found for `<strong>{0}</strong>`'.format(selected))
            return
        if (len(panel_items) == 1):
            self.view.run_command('do_insert_import', {'item': match_items[0]})
            return
        self.view.window().show_quick_panel(panel_items, on_done_func(match_items, self.on_select))
        
    def on_select(selected_item):
        debug('Selected item', selected_item)
        self.view.run_command('do_insert_import', {'item': selected_item})
    
# =============================================== Command list_imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    # Show all available imports
    def __init__(self, view):
        super().__init__(view)
        self.import_root = get_import_root()

    def run(self, edit):
        match_items = []
        panel_items = []
        for item in source_modules:
            match_items.append(item)
            panel_items.append(get_panel_item(self.import_root, item))
        for item in node_modules:
            match_items.append(item)
            panel_items.append(get_panel_item(self.import_root, item))
        self.view.window().show_quick_panel(panel_items, on_done_func(match_items, self.on_select))

    def on_select(self, selected_item):
        debug('Selected item', selected_item)
        self.view.run_command('do_insert_import', {'item': selected_item})

# window.run_command('update_imports')
# sublime.active_window().run_command('update_imports', args={'a':'bar'})
class UpdateImportsCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()

# view.run_command('import_from_clipboard')
class ImportFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_import', args=({'selected': sublime.get_clipboard()}))

class UpdateSourceEventListener(sublime_plugin.EventListener):
    
    def __init__(self):
        self.viewIds = []

    def on_new(self, view):
        self.viewIds.append(view.id())

    def on_post_save(self, view):
        if view.id() in self.viewIds:
            self.viewIds.remove(view.id())
            update_source_modules()

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

