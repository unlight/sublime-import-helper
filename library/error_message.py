import sublime
from ..import_helper import PROJECT_NAME


def error_message(err):
    sublime.error_message(PROJECT_NAME + "\n" + str(err))
