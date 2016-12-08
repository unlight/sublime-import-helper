import sublime
import sublime_plugin
import os
import platform
import subprocess
import threading
import socket

# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)

DEBUG_NO_SHUTDOWN = True
DEBUG_MESSAGES = True

PROJECT_NAME = "import-helper"
SETTINGS_FILE = PROJECT_NAME + ".sublime-settings"
# KEYMAP_FILE = "Default ($PLATFORM).sublime-keymap"
# IS_WINDOWS = platform.system() == 'Windows'
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__));
SERVER_PATH = "server/main.js"
SETUP_PATH = "server/setup.js"
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 6778

PROJECT_DIRECTORY = None
settings = sublime.load_settings(SETTINGS_FILE)
# TODO: Load and get settings value = settings.get("name")

SOURCE_ROOT = None

def debug(s, data = None, force = False):
    if (DEBUG_MESSAGES or force == True):
        message = str(s)
        if (data is not None):
            message = message + ': ' + str(data)
        print(message)

def status_message(message):
    sublime.status_message(message)

def setup_callback(err, result):
    if (bool(err)): return
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
    
    serverCmd = ["node", SERVER_PATH, str(SERVER_PORT)]
    debug("Starting server", " ".join(serverCmd))
    exec_async(serverCmd)
    sublime.set_timeout(initialize_project, 800)

def read_packages_callback(err, result):
    if (bool(err) == False):
        debug('Read packages result', len(result))

def initialize_project():
    data = {'projectDirectory': SOURCE_ROOT}
    send_command_async("read_packages", data, read_packages_callback)

def send_command_async(command, data = None, callback = None):
    thread = threading.Thread(target=send_command, args=(command, data, callback))
    thread.daemon = True
    thread.start()

def send_command(command, data = None, callback = None):
    debug("Send command", command)
    client = socket.socket()
    recv = ""
    try:
        client.connect((SERVER_ADDRESS, SERVER_PORT))
        message = sublime.encode_value({"command": command, "data": data}, True)
        client.send(message.encode('utf-8'))
        recv = client.recv(128 * 1024).decode('utf-8')
        client.close()
    except Exception as err:
        debug("Send command error", err)
        callback(err, None)
        return
    response = None
    if (bool(recv)):
        debug("Trying to parse", recv)
        response = sublime.decode_value(recv)
    if callback is not None:
        callback(None, response)
        return
    return response

def exec(cmd):
    if os.name == "nt":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(cmd, cwd=PACKAGE_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=si)
    else:
        proc = subprocess.Popen(cmd, cwd=PACKAGE_PATH, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate()
    err = errs.decode().strip();
    if (bool(err)):
        debug("Exec error", err)
    return (err, outs.decode().strip())

def exec_async(cmd, done=None):
    def runInThread(cmd, done):
        (err, result) = exec(cmd)
        if (done is not None):
            done(err, result)
        return
    thread = threading.Thread(target=runInThread, args=(cmd, done))
    thread.start()
    return thread

# =============================================== Plugin Lifecycle

def plugin_loaded():
    print()
    debug("Plugin loaded", PROJECT_NAME)
    exec_async(["node", SETUP_PATH], setup_callback)
    
def plugin_unloaded():
    if DEBUG_NO_SHUTDOWN: return
    debug("Plugin unloaded, kill server", PROJECT_NAME)
    send_command("shutdown")
    
# =============================================== sublime_plugin.EventListener

class EventListener(sublime_plugin.EventListener):

    def on_close(self, view):
        if DEBUG_NO_SHUTDOWN: return
        window = sublime.active_window()
        if window is None or not window.views():
            send_command("shutdown")

# =============================================== Command insert_import_statement

class InsertImportStatementCommand(sublime_plugin.TextCommand):
    """ Adds import of identifier near cursor """
    def run(self, edit):
        view = self.view
        selected_region = view.sel()[0]
        selected_str = view.substr(selected_region)
        if (bool(selected_str) == False):
            cursor_region = view.expand_by_class(selected_region, sublime.CLASS_WORD_START | sublime.CLASS_WORD_END)
            selected_str = view.substr(cursor_region)
        debug("selected_str", selected_str)
        statements = send_command("insert_import_statement", selected_str)
        items = []
        item_modules = []
        for item in statements:
            if (item['name'] == selected_str):
                items.append(item)
                module_path = item['module']
                # if (module_path[0:2] == './'): module_path = module_path[2:]
                if (module_path[-3:] == '.ts'): module_path = module_path[0:-3]
                item_modules.append(module_path)
                item['module_path'] = module_path
                
        if (len(item_modules) == 0):
            view.show_popup("No imports found for `<strong>{0}</strong>`".format(selected_str))
        # debug('statements', statements)
        # def on_navigate(href):
        #     debug('on_navigate href', href);
        # if (len(item_modules) > 0):
        #     import_items = "\n".join(['<a href="{0}">{0}</a>'.format(item['module']) for item in statements])
        #     debug('import_items', import_items)
        #     view.show_popup("<body>Import <strong>{0}</strong> from:\n{1}</body>".format(selected_str, import_items),
        #         on_navigate=on_navigate, max_width=500)
        # if (len(item_modules) > 0):

        if (len(item_modules) > 0):
            window = view.window()
            def on_select(selected_index):
                debug('Selected index', selected_index)
                if (selected_index == -1): return
                selected_item = items[selected_index]
                debug('Selected item', selected_item)
                view.run_command('do_insert_import_statement', {'item': selected_item})
            window.show_quick_panel(item_modules, on_select)

# TEST: connection Author Photo PhotoMetadata Date
class DoInsertImportStatementCommand(sublime_plugin.TextCommand):
    def run(self, edit, item):
        module_path = item['module_path']
        import_string = "import {{ {0} }} from '{1}';\n".format(
            item['name'], module_path
        )
        debug('Import string', import_string)
        pos = 0
        self.view.insert(edit, pos, import_string)
