import sublime
import sublime_plugin
from .utils import *

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

PROJECT_NAME = 'Import Helper'
node_modules = []
source_modules = []
typescript_paths = []

# Plugin Lifecycle

def plugin_loaded():
    print()
    debug('Plugin loaded', PROJECT_NAME)
    sublime.set_timeout(initialize, 0)
    sublime.set_timeout(setup, 0)

def setup():
    project_file = sublime.active_window().project_file_name()
    if project_file is None:
        message = 'There is no project file, {0} will not work without project.'.format(PROJECT_NAME)
        debug(message, force=True)
        sublime.status_message(message)
        return
    update_source_modules()
    update_node_modules()
    update_typescript_paths()

def update_source_modules():
    source_folders = get_source_folders()
    debug('source_folders', source_folders)
    def get_source_modules_callback(err, result):
        if err:
            sublime.error_message(PROJECT_NAME + '\n' + str(err))
            return
        source_modules.clear();
        exclude_patterns = get_exclude_patterns()
        if type(result) is not list:
            sublime.error_message(PROJECT_NAME + '\n' + 'Unexpected type of result: ' + type(result))
            return
        for item in result:
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

def update_typescript_paths():
    typescript_paths.clear()
    # source_folders = get_source_folders()
    source_folders = [get_import_root()]
    for folder in source_folders:
        tsconfig_file = os.path.normpath(os.path.join(folder, 'tsconfig.json'))
        if not os.path.isfile(tsconfig_file):
            continue
        tsconfig = read_json(tsconfig_file) or {}
        compilerOptions = tsconfig.get('compilerOptions')
        if compilerOptions is None:
            continue
        baseUrl = compilerOptions.get('baseUrl')
        if baseUrl is None:
            continue
        base_dir = os.path.normpath(os.path.join(os.path.dirname(tsconfig_file), baseUrl))
        paths = compilerOptions.get('paths')
        for path_to, pathValues in paths.items():
            for path_value in pathValues:
                typescript_paths.append({'base_dir': base_dir, 'path_value': path_value, 'path_to': path_to})
    debug('typescript_paths', typescript_paths)

def get_modules_callback(err, result):
    if err:
        sublime.error_message(PROJECT_NAME + '\n' + str(err))
        return
    if type(result) is not list:
        sublime.error_message(PROJECT_NAME + '\n' + 'Unexpected type of result: ' + type(result))
        return
    node_modules.extend(result)
    sublime.status_message('{0}: {1} node modules found'.format(PROJECT_NAME, len(node_modules)))
    debug('Get packages result', len(result))

# Command insert_import
class InsertImportCommand(sublime_plugin.TextCommand):
    # Adds import of identifier near cursor

    def run(self, edit, name=None, point=None):
        if name is None:
            point_region = self.view.sel()[0]
            if point is not None:
                point_region = sublime.Region(point, point)
            name = self.view.substr(point_region).strip()
            if not bool(name):
                cursor_region = self.view.expand_by_class(point_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
                name = self.view.substr(cursor_region)
                name = name.strip()
        debug('Trying to import', '`' + name + '`')
        import_root = get_import_root()
        match_items = []
        panel_items = []
        # Iterate through source modules + node modules
        for item in source_modules + node_modules:
            if (item.get('name') == name):
                panel_item = get_panel_item(import_root, item)
                if panel_item is not None:
                    panel_items.append(panel_item)
                    match_items.append(item)
        if (len(panel_items) == 0):
            self.view.show_popup('No imports found for `<strong>{0}</strong>`'.format(name))
            return
        if (len(panel_items) == 1):
            self.view.run_command('do_insert_import', {'item': match_items[0], 'typescript_paths': typescript_paths})
            return
        on_done = on_done_func(match_items, self.on_select)
        self.view.window().show_quick_panel(panel_items, on_done)
        
    def on_select(self, selected_item):
        debug('Selected item', selected_item)
        self.view.run_command('do_insert_import', {'item': selected_item, 'typescript_paths': typescript_paths})
    
# Command list_imports
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
        self.view.run_command('do_insert_import', {'item': selected_item, 'typescript_paths': typescript_paths})

# window.run_command('initialize_setup')
# sublime.active_window().run_command('initialize_setup', args={'a':'bar'})
class InitializeSetupCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()

# window.run_command('update_source_modules')
class UpdateSourceModulesCommand(sublime_plugin.WindowCommand):
    
    def run(self):
        update_source_modules()

# Command import_from_clipboard
# view.run_command('import_from_clipboard')
class ImportFromClipboardCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command('insert_import', args=({'name': sublime.get_clipboard()}))

# ImportHelperEventListener
class ImportHelperViewEventListener(sublime_plugin.EventListener):

    def __init__(self):
        self.viewIds = []

    def on_new(self, view):
        self.viewIds.append(view.id())

    def on_post_save(self, view):
        if view.id() in self.viewIds:
            self.viewIds.remove(view.id())
            update_source_modules()

# ImportHelperViewEventListener
class ImportHelperViewEventListener(sublime_plugin.ViewEventListener):

    def __init__(self, view):
        super().__init__(view)
        self.completions_info = {'time': -1, 'result': [], 'prefix': ''}
        self.in_auto_complete = False

    def on_query_completions(self, prefix, locations):
        if not (len(prefix) > 0 and self.view.match_selector(locations[0], 'source.ts, source.tsx, source.js, source.jsx')):
            return []
        if get_time() > self.completions_info['time'] + 1 or prefix != self.completions_info['prefix']:
            # debug('on_query_completions', [prefix, locations])
            self.completions_info['time'] = get_time()
            self.completions_info['prefix'] = prefix
            self.completions_info['result'] = query_completions_modules(prefix, source_modules, node_modules)
        return self.completions_info['result']
    
    def on_post_text_command(self, command_name, args):
        if self.in_auto_complete and (command_name == 'insert_best_completion' or command_name == 'insert_dimensions'):
            self.in_auto_complete = False
            self.view.run_command('insert_import')
        elif command_name == 'auto_complete' or command_name == 'replace_completion_with_next_completion' or command_name == 'replace_completion_with_auto_complete':
            self.in_auto_complete = True
        elif command_name == 'hide_auto_complete':
            self.in_auto_complete = False
        # debug('after on_post_text_command', [command_name, args, 'self.in_auto_complete', self.in_auto_complete])

    def on_activated(self):
        # debug('on_activated')
        self.in_auto_complete = False
