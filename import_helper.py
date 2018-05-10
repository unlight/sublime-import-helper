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
        sublime.error_message('{0}:\n{1}'.format(PROJECT_NAME, str(err)))
        return
    if type(result) is not list:
        sublime.error_message('{0}:\nUnexpected type of result: {1}'.format(PROJECT_NAME, type(result)))
        return
    node_modules.extend(result)
    sublime.status_message('{0}: {1} node modules found'.format(PROJECT_NAME, len(node_modules)))
    debug('Get packages result', len(result))

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
        self.auto_complete_point = 0

    def on_query_completions(self, prefix, locations):
        self.auto_complete_point = locations[0]
        if not (len(prefix) > 0 and self.view.match_selector(self.auto_complete_point, 'source.ts, source.tsx, source.js, source.jsx')):
            return []
        if get_time() > self.completions_info['time'] + 1 or prefix != self.completions_info['prefix']:
            self.completions_info['time'] = get_time()
            self.completions_info['prefix'] = prefix
            self.completions_info['result'] = query_completions_modules(prefix, source_modules, node_modules)
        return self.completions_info['result']
    
    def on_post_text_command(self, command_name, args):
        if self.in_auto_complete and command_name in ['insert_best_completion', 'insert_dimensions']:
            self.in_auto_complete = False
            self.view.run_command('insert_import', args=({'point': self.auto_complete_point - 1}))
        elif command_name in ['auto_complete', 'replace_completion_with_next_completion', 'replace_completion_with_auto_complete']:
            self.in_auto_complete = True
        elif command_name == 'hide_auto_complete':
            self.in_auto_complete = False

    def on_activated(self):
        self.in_auto_complete = False
