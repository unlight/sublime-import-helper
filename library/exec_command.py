import sublime
import os
import subprocess
import threading
import traceback

from ..import_helper import RUN_PATH, NODE_BIN, PACKAGE_PATH
from .debug import debug


def run_command(command, data=None, callback=None):
    debug("run_command", [NODE_BIN, command, data])
    json = sublime.encode_value({"command": command, "args": data})
    err = None
    out = None
    try:
        (err, out) = exec([NODE_BIN, "--no-warnings", RUN_PATH], json)
    except Exception as e:
        err = traceback.format_exc()
    if bool(err):
        if callback is not None:
            return callback(err, None)
        raise Exception(err)
    # debug('run_command: trying to decode', out)
    result = sublime.decode_value(out)
    if callback is not None:
        return callback(None, result)
    return result


def run_command_async(command, data=None, callback=None):
    thread = threading.Thread(target=run_command, args=(command, data, callback))
    thread.start()


def exec(cmd, input):
    if os.name == "nt":
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.SW_HIDE | subprocess.STARTF_USESHOWWINDOW
        proc = subprocess.Popen(
            cmd,
            cwd=PACKAGE_PATH,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=si,
        )
    else:
        proc = subprocess.Popen(
            cmd,
            cwd=PACKAGE_PATH,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    if type(input) == str:
        input = input.encode()
    outs, errs = proc.communicate(input=input)
    err = errs.decode().strip()
    if bool(err):
        debug("Exec error", err, True)
    return (err, outs.decode().strip())
