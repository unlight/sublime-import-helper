import sublime
import os
import sys
import platform
import subprocess
import threading
import socket
import traceback
import fnmatch

DEBUG = True
DEBUG = False
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
RUN_PATH = os.path.join(PACKAGE_PATH, 'backend_run.js')
if DEBUG: RUN_PATH = os.path.join(PACKAGE_PATH, 'backend', 'run.js')
NODE_BIN = 'node'

def initialize():
    global NODE_BIN
    if NODE_BIN == 'node' or not bool(NODE_BIN):
        NODE_BIN = get_setting('node_bin', '')
        if not bool(NODE_BIN): NODE_BIN = find_executable('node')
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
    debug('Trying to decode', out)
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
    if (module is not None):
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

def get_exclude_patterns():
    result = []
    project_data = sublime.active_window().project_data()
    project_file = sublime.active_window().project_file_name()
    for folder in project_data['folders']:
        folder_exclude_patterns = folder.get('folder_exclude_patterns')
        if folder_exclude_patterns is None: folder_exclude_patterns = []
        for pattern in folder_exclude_patterns:
            result.append(pattern)
        file_exclude_patterns = folder.get('file_exclude_patterns')
        if file_exclude_patterns is None: file_exclude_patterns = []
        for pattern in file_exclude_patterns:
            result.append(pattern)
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
    for folder in project_data['folders']:
        folder_path = folder['path']
        path_source = project_data.get('path_source')
        if bool(path_source):
            folder_path = path_source
        folder_path = norm_path(project_file, folder_path)
        result.append(folder_path)
    return result