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
    def get_source_modules_callback(err, modules):
        if err:
            sublime.error_message(PROJECT_NAME + '\n' + str(err))
            return
        source_modules.clear();
        exclude_patterns = get_exclude_patterns()
        if type(modules) is not list:
            sublime.error_message(PROJECT_NAME + '\n' + 'Unexpected type of result: ' + type(modules))
            return
        for item in modules:
            filepath = item.get('filepath')
            if filepath is None: continue
            if is_excluded_file(filepath, exclude_patterns): continue
            source_modules.append(item)
        sublime.status_message('{0}: {1} source modules found'.format(PROJECT_NAME, len(source_modules)))
        debug('Update source modules', len(source_modules))
    run_command_async('get_folders', {'folders': source_folders}, get_source_modules_callback)

def update_node_modules():
    node_modules.clear()
    import_root = get_import_root()
    debug('import_root', import_root)
    run_command_async('get_modules', {'importRoot': import_root, 'packageKeys': ['devDependencies']}, get_modules_callback)
    run_command_async('get_modules', {'importRoot': import_root, 'packageKeys': ['dependencies']}, get_modules_callback)

def get_exclude_patterns():
    result = []
    project_data = sublime.active_window().project_data()
    project_file = sublime.active_window().project_file_name()
    for folder in project_data['folders']:
        folder_exclude_patterns = folder.get('folder_exclude_patterns')
        if folder_exclude_patterns is None: folder_exclude_patterns = []
        for pattern in folder_exclude_patterns:
            result.append(norm_path(project_file, pattern))
        file_exclude_patterns = folder.get('file_exclude_patterns')
        if file_exclude_patterns is None: file_exclude_patterns = []
        for pattern in file_exclude_patterns:
            result.append(norm_path(project_file, pattern))
    return result

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

def get_modules_callback(err, result):
    if err:
        sublime.error_message(PROJECT_NAME + '\n' + str(err))
        return
    if type(result) is list:
        node_modules.extend(result)
    sublime.status_message('{0}: {1} node modules found'.format(PROJECT_NAME, len(node_modules)))
    debug('Get packages result', len(result))

# =============================================== Plugin Lifecycle

def plugin_loaded():
    print()
    debug('Plugin loaded', PROJECT_NAME)
    sublime.set_timeout(initialize, 0)
    sublime.set_timeout(setup, 0)

# =============================================== Command insert_import

class InsertImportCommand(sublime_plugin.TextCommand):
    # Adds import of identifier near cursor

    def run(self, edit, selected=None):
        if (selected is None):
            selected_region = self.view.sel()[0]
            selected = self.view.substr(selected_region)
        if not bool(selected):
            cursor_region = self.view.expand_by_class(selected_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            selected = self.view.substr(cursor_region)
        debug('Selected word region', selected)
        import_root = get_import_root()
        match_items = []
        panel_items = []
        # Iterate through source modules + node modules
        for item in source_modules + node_modules:
            if (item.get('name') == selected):
                panel_item = get_panel_item(import_root, item)
                if panel_item is not None:
                    panel_items.append(panel_item)
                    match_items.append(item)
        if (len(panel_items) == 0):
            self.view.show_popup('No imports found for `<strong>{0}</strong>`'.format(selected))
            return
        if (len(panel_items) == 1):
            self.view.run_command('do_insert_import', {'item': match_items[0]})
            return
        on_done = on_done_func(match_items, self.on_select)
        self.view.window().show_quick_panel(panel_items, on_done)
        
    def on_select(self, selected_item):
        debug('Selected item', selected_item)
        self.view.run_command('do_insert_import', {'item': selected_item})
    
# =============================================== Command list_imports
# view.run_command('list_imports')
class ListImportsCommand(sublime_plugin.TextCommand):
    # Show all available imports

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
        debug('Selected item', selected_item)
        self.view.run_command('do_insert_import', {'item': selected_item})

# window.run_command('update_imports')
# sublime.active_window().run_command('update_imports', args={'a':'bar'})
class UpdateImportsCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()

# window.run_command('update_source_modules')
class UpdateSourceModulesCommand(sublime_plugin.WindowCommand):
    
    def run(self):
        update_source_modules()

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

