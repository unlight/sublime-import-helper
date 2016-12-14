import sublime
import os
import platform
import subprocess
import threading
import socket

DEBUG_MESSAGES = True
PACKAGE_PATH = os.path.dirname(os.path.realpath(__file__))
RUN_PATH = "backend/run.js"
SERVER_PATH = "backend/server.js"
SETUP_PATH = "backend/setup.js"
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 6778

def debug(s, data = None, force = False):
    if (DEBUG_MESSAGES or force == True):
        message = str(s)
        if (data is not None):
            message = message + ': ' + str(data)
        print(message)
        
def status_message(message):
    sublime.status_message(message)
    
def run_command(command, data = None, callback = None):
    debug("Run command", command)
    json = sublime.encode_value(data)
    (err, out) = exec(["node", RUN_PATH, command, json])
    if (bool(err)):
        if callback is not None:
            return callback(err, None)
        raise err
    debug("Trying to decode", out)
    result = sublime.decode_value(out)
    if callback is not None:
        return callback(None, result)
    return result

def run_command_async(command, data = None, callback = None):
    thread = threading.Thread(target=run_command, args=(command, data, callback))
    thread.daemon = True
    thread.start()
    
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
    
def unixify(path):
    path = path.replace('\\', '/')
    if (path[-3:] == '.ts'): 
        path = path[0:-3]
    return path
    
def get_panel_item(root, item):
    module = item.get('module')
    if (module is not None):
        return module + '/' + item['name']
    filepath = os.path.normpath(item['filepath'])[len(root) + 1:]
    return unixify(filepath) + '/' + item['name']
    
