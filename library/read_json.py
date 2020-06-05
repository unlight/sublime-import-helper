import sublime
import os


def read_json(file):
    if not os.path.isfile(file):
        return None
    fo = open(file, "r")
    data = fo.read()
    fo.close()
    return sublime.decode_value(data)
