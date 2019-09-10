import sublime
import sublime_plugin
import concurrent.futures
from .utils import *

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

PROJECT_NAME = 'Import Helper'
node_modules = [] # Collection of entries
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
        if type(result) is not list:
            sublime.error_message(PROJECT_NAME + '\n' + 'Unexpected type of result: ' + type(result))
            return
        for item in result:
            filepath = item.get('filepath')
            if filepath is None: continue
            source_modules.append(item)
        sublime.status_message('{0}: {1} source modules found'.format(PROJECT_NAME, len(source_modules)))
        debug('Update source modules', len(source_modules))
    exclude_patterns = get_exclude_patterns()
    run_command_async('get_folders', { 'folders': source_folders, 'ignore': exclude_patterns }, get_source_modules_callback)

def update_node_modules():
    node_modules.clear()
    import_root = get_import_root()
    debug('update_node_modules: import_root', import_root)
    is_loading = True
    loading_module_name = None

    def load_module_timer():
        nonlocal is_loading, loading_module_name
        if is_loading:
            if loading_module_name is not None:
                sublime.status_message('{0}: Processing {1}...'.format(PROJECT_NAME, loading_module_name))
            sublime.set_timeout(load_module_timer, 1000)

    def load_module(name):
        nonlocal loading_module_name
        loading_module_name = name
        result = run_command('get_module', {'importRoot': import_root, 'name': name})
        get_modules_callback(None, result, {'name': name, 'count': len(result)})

    def get_from_package_callback(err, result):
        nonlocal is_loading
        if err:
            sublime.error_message('{0}:\n{1}'.format(PROJECT_NAME, str(err)))
            return
        if type(result) is not list:
            sublime.error_message('{0}:\nUnexpected type of result: {1}'.format(PROJECT_NAME, type(result)))
            return
        node_modules_names = set(())
        for name in result:
            if type(name) == str and len(name) > 0:
                node_modules_names.add(name)
        debug('get_from_package_callback: node_modules_names', node_modules_names)
        for name in node_modules_names:
            node_modules.append({'module': name, 'name': name, 'isDefault': True, 'from_package': True})
        load_module_timer()
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            futures = [executor.submit(load_module, name) for name in node_modules_names]
            concurrent.futures.wait(futures, timeout=None, return_when=concurrent.futures.ALL_COMPLETED)
            # future_to_name = {executor.submit(load_module, name): name for name in node_modules_names}
            is_loading = False
            loading_module_name = None
            debug('Stopped processing node modules')

    run_command_async('get_from_package', {'importRoot': import_root}, get_from_package_callback)

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
        if not paths:
            continue
        for path_to, pathValues in paths.items():
            for path_value in pathValues:
                typescript_paths.append({'base_dir': base_dir, 'path_value': path_value, 'path_to': path_to})
    debug('typescript_paths', typescript_paths)

def get_modules_callback(err, result, sender = None):
    if err:
        sublime.error_message('{0}:\n{1}'.format(PROJECT_NAME, str(err)))
        return
    if type(result) is not list:
        sublime.error_message('{0}:\nUnexpected type of result: {1}'.format(PROJECT_NAME, type(result)))
        return
    node_modules.extend(result)
    message = '{0}: {1} node modules found'.format(PROJECT_NAME, len(node_modules))
    if sender is not None:
        message = message + ', {0} +{1}'.format(sender['name'], sender['count'])
    sublime.status_message(message)
    debug('get_modules_callback: len(result)', len(result))

# window.run_command('initialize_setup')
# sublime.active_window().run_command('initialize_setup', args={'a':'bar'})
class InitializeSetupCommand(sublime_plugin.WindowCommand):
    def run(self):
        setup()

# window.run_command('update_source_modules')
class UpdateSourceModulesCommand(sublime_plugin.WindowCommand):

    def run(self):
        update_source_modules()

