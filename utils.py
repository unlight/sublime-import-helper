import sublime
import os
import sys
import platform
import subprocess
import threading
import socket
import traceback
import fnmatch
import time
import re

DEBUG = True
DEBUG = False
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
RUN_PATH = os.path.join(PACKAGE_PATH, 'backend_run.js')
if DEBUG:
    RUN_PATH = os.path.join(PACKAGE_PATH, 'backend', 'run.js')
NODE_BIN = 'node'

def initialize():
    global NODE_BIN
    if NODE_BIN == 'node' or not bool(NODE_BIN):
        NODE_BIN = get_setting('node_bin', '')
        if not bool(NODE_BIN):
            NODE_BIN = find_executable('node')
        if not bool(NODE_BIN): NODE_BIN = 'node'

def debug(s, data=None, force=False):
    if (DEBUG or force):
        message = str(s)
        if (data is not None):
            message = message + ': ' + str(data)
        print(message)

def run_command(command, data=None, callback=None):
    global NODE_BIN
    debug('Run command', [NODE_BIN, command, data])
    json = sublime.encode_value(data)
    err = None
    out = None
    try:
        (err, out) = exec([NODE_BIN, RUN_PATH, command, json])
    except Exception as e:
        err = traceback.format_exc()
    if bool(err):
        if callback is not None:
            return callback(err, None)
        raise err
    # debug('run_command: trying to decode', out)
    result = sublime.decode_value(out)
    if callback is not None:
        return callback(None, result)
    return result

def run_command_async(command, data=None, callback=None):
    thread = threading.Thread(target=run_command, args=(command, data, callback))
    thread.start()

def exec(cmd):
    if os.name == 'nt':
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(cmd, cwd=PACKAGE_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
    else:
        proc = subprocess.Popen(cmd, cwd=PACKAGE_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()
    err = errs.decode().strip()
    if bool(err):
        debug('Exec error', err, True)
    return (err, outs.decode().strip())

def exec_async(cmd, done=None):
    def run_thread(cmd, done):
        (err, result) = exec(cmd)
        if (done is not None):
            done(err, result)
        return
    thread = threading.Thread(target=run_thread, args=(cmd, done))
    thread.start()
    return thread

def unixify(path):
    path = path.replace('\\', '/')
    ext3 = path[-3:]
    if (ext3 == '.ts' or ext3 == '.js'):
        return path[0:-3]
    ext4 = path[-4:]
    if (ext4 == '.tsx' or ext4 == '.jsx'):
        return path[0:-4]
    return path

def get_panel_item(root, item):
    # Prepare string to show in window's quick panel.
    module = item.get('module')
    name = item.get('name')
    # TODO: Handle case when name is none (browserify)
    if name is None:
        return None
    if module is not None:
        if module == name and item.get('isDefault') == True:
            return module + '/default'
        return module + '/' + name
    filepath = os.path.normpath(item['filepath'])[len(root) + 1:]
    return unixify(filepath) + '/' + name

def norm_path(base, to):
    return os.path.normpath(os.path.join(os.path.dirname(base), to))

def on_done_func(choices, func):
    # Return a function which is used with sublime list picking.
    def on_done(index):
        if index >= 0:
            return func(choices[index])
    return on_done

def is_excluded_file(filepath, exclude_patterns):
    if exclude_patterns is None or len(exclude_patterns) == 0:
        return False
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(filepath, pattern): return True
        if not os.path.isabs(pattern):
            if fnmatch.fnmatch(filepath, os.path.normpath('*/' + pattern + '/*')): return True
            if fnmatch.fnmatch(filepath, os.path.normpath('*/' + pattern)): return True
            if fnmatch.fnmatch(filepath, os.path.normpath(pattern + '/*')): return True
    return False

def get_setting(name, default):
    result = None
    project_data = sublime.active_window().project_data()
    if project_data is not None:
        result = project_data.get(name)
    if result is None:
        settings = sublime.load_settings('import_helper.sublime-settings') or {}
        result = settings.get(name)
    if result is None:
        preferences = sublime.load_settings('Preferences.sublime-settings')
        result = preferences.get(name)
    if result is None:
        result = default
    return result

def get_import_root():
    window = sublime.active_window()
    project_file = window.project_file_name()
    if project_file is None:
        return None
    project_data = window.project_data() or {}
    result = project_data.get('import_root')
    if result is None:
        result = project_data['folders'][0]['path']
    return norm_path(project_file, result)

# https://gist.github.com/4368898
# Public domain code by anatoly techtonik <techtonik@gmail.com>
# AKA Linux `which` and Windows `where`
def find_executable(executable, path = None):
    """Find if 'executable' can be run. Looks for it in 'path'
    (string that lists directories separated by 'os.pathsep';
    defaults to os.environ['PATH']). Checks for all executable
    extensions. Returns full path or None if no command is found.
    """
    if path is None:
        path = os.environ['PATH']
    paths = path.split(os.pathsep)
    extlist = ['']
    if os.name == 'os2':
        (base, ext) = os.path.splitext(executable)
        # executable files on OS/2 can have an arbitrary extension, but
        # .exe is automatically appended if no dot is present in the name
        if not ext:
            executable = executable + '.exe'
    elif sys.platform == 'win32':
        pathext = os.environ['PATHEXT'].lower().split(os.pathsep)
        (base, ext) = os.path.splitext(executable)
        if ext.lower() not in pathext:
            extlist = pathext
    for ext in extlist:
        execname = executable + ext
        if os.path.isfile(execname):
            return execname
        else:
            for p in paths:
                f = os.path.join(p, execname)
                if os.path.isfile(f):
                    return f
    else:
        return None

def get_exclude_patterns(project_data = None, project_file = None):
    if project_data is None:
        project_data = sublime.active_window().project_data()
    if project_file is None:
        project_file = sublime.active_window().project_file_name()
    result = {}
    for folder in ((project_data or {}).get('folders') or []):
        exclude_patterns = []
        folder_exclude_patterns = folder.get('folder_exclude_patterns')
        if folder_exclude_patterns is None:
            folder_exclude_patterns = []
        for pattern in folder_exclude_patterns:
            exclude_patterns.append(pattern)
        file_exclude_patterns = folder.get('file_exclude_patterns')
        if file_exclude_patterns is None:
            file_exclude_patterns = []
        for pattern in file_exclude_patterns:
            exclude_patterns.append(pattern)
        binary_file_patterns = folder.get('binary_file_patterns')
        if binary_file_patterns is None:
            binary_file_patterns = []
        for pattern in binary_file_patterns:
            exclude_patterns.append(pattern)
        if len(exclude_patterns) > 0:
            path = folder.get('path')
            path = norm_path(project_file, path)
            result[path] = exclude_patterns
    return result

def read_json(file):
    if not os.path.isfile(file):
        return None
    fo = open(file, 'r')
    data = fo.read()
    fo.close()
    return sublime.decode_value(data)

def get_source_folders():
    window = sublime.active_window()
    project_file = window.project_file_name()
    project_data = window.project_data()
    result = []
    for folder in (project_data.get('folders') or []):
        folder_path = folder.get('path')
        if folder_path is None:
            continue
        path_source = project_data.get('path_source')
        if bool(path_source):
            folder_path = path_source
        folder_path = norm_path(project_file, folder_path)
        result.append(folder_path)
    return result

def get_time():
    return time.time()

def query_completions_modules(prefix, source_modules, node_modules):
    result = []
    for item in source_modules:
        name = item.get('name')
        if name is None:
            continue
        if not name.startswith(prefix):
            continue
        result.append([name + '\tsource_modules', name])
    for item in node_modules:
        name = item.get('name')
        module = item.get('module')
        if name is None or module is None:
            continue
        if not name.startswith(prefix):
            continue
        result.append([name + '\tnode_modules/' + module, name])
    return result

def is_import_all(string):
    return re.match(r"^import\s+\*\s+as\s+(.+)\s+from\s+(['\"])(.+)\2", string)

def is_import_default(string):
    return re.match(r"^import\s+([^ ,{}]+)\s+from\s+(['\"])(.+)\2", string)

# https://github.com/ecrmnn/camelcase
def camelcase(*arguments):
    if type(arguments[0]) == list:
        # Arguments passed as list
        string = '_'.join(arguments[0])
    elif len(arguments) != 1:
        # Multiple arguments passed (variadict)
        string = '_'.join(list(arguments))
    else:
        # Argument was a string
        string = arguments[0]

    items = re.split(r'\-|\_|\s', string)
    items = list(filter(None, items))

    titleCased = map(lambda item: item.lower().title(), items[1:])

    return items[0].lower() + ''.join(titleCased)

def get_identifier_name(text):
    return camelcase(text)

def try_typescript_path(filepath, typescript_paths):
    import_path_mapping = get_setting('import_path_mapping', 'none')
    if import_path_mapping == 'enabled':
        (drive, filepath) = os.path.splitdrive(filepath)
        filepath = filepath.replace('\\', '/')
        # debug("filepath", filepath)
        for ts_path in typescript_paths:
            base_dir = ts_path['base_dir']
            path_value = ts_path['path_value']
            path_to = ts_path['path_to']
            (drive, test_path) = os.path.splitdrive(os.path.normpath(os.path.join(base_dir, path_value)).replace('\\', '/'))
            # debug("test_path", test_path)
            # "@app/*" :["app/*"]
            if test_path[-2:] == '/*' and path_to[-2:] == '/*':
                test_path = test_path[0:-2]
                if filepath.startswith(test_path):
                    test_path = path_to[0:-2] + filepath[len(test_path):]
                    return test_path
            # "@lib": ["app/lib"]
            if filepath == test_path or filepath in [test_path + '/index.ts', test_path + '/index.tsx', test_path + '/index.js', test_path + '/index.jsx']:
                return path_to
    return None

# Check if possible insert name multiple ways (different paths)
def get_from_paths(item, file_name = None, typescript_paths = []):
    if (item.get('module')):
        from_path = item['module']
        return [from_path]
    if not file_name:
        file_name = '.'
    from_path = os.path.relpath(item['filepath'], os.path.dirname(file_name))
    from_path = unixify(from_path)
    if from_path[0] != '.':
        from_path = './' + from_path
    result = [from_path]
    typescript_path = try_typescript_path(item['filepath'], typescript_paths)
    if typescript_path is not None:
        typescript_path = unixify(typescript_path)
        result.insert(0, typescript_path)
    remove_trailing_index = get_setting('remove_trailing_index', True)
    for i, from_path in enumerate(result):
        if remove_trailing_index and from_path[-6:] == '/index':
            result[i] = from_path[:-6]
    return result

def wrap_imports(imports):
    start = '{'
    end = '}'
    if get_setting('space_around_braces', True):
        start = start + ' '
        end = ' ' + end
    return start + ', '.join(imports) + end

def get_import_line_info(view, from_path):
    row = 0
    import_row = -1 # initial value -1 not found
    last_row = view.rowcol(view.size())[0]
    no_match_count = 0
    last_import_row = -1
    while row <= last_row:
        line_region = view.full_line(view.text_point(row, 0))
        line_contents = view.substr(line_region)
        match = re.search(r"^import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
        if match:
            last_import_row = row
            no_match_count = 0
            if match.group(3) == from_path:
                import_row = row
                break
        else:
            no_match_count = no_match_count + 1
        # Break loop if cannot find 3+ lines with import
        if no_match_count >= 3:
            break
        # Go to next line
        row = row + 1
    imports = []
    if import_row != -1:
        for m in re.finditer(r"(\w+(\s+as\s+\w+)?)", match.group(1)):
            imports.append(m.group(1))
    return {'import_row': import_row, 'imports': imports, 'from_path': from_path, 'last_import_row': last_import_row, 'line_contents': line_contents}
