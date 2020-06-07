import sublime
import os
import time

from ..import_helper import PROJECT_NAME


def norm_path(base, to):
    return os.path.normpath(os.path.join(os.path.dirname(base), to))


def get_time():
    return time.time()


def error_message(err):
    sublime.error_message(PROJECT_NAME + "\n" + str(err))


def status_message(string):
    sublime.status_message("{0}: {1}".format(PROJECT_NAME, string))
