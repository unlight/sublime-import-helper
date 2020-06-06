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


# def is_excluded_file(filepath, exclude_patterns):
#     if exclude_patterns is None or len(exclude_patterns) == 0:
#         return False
#     for pattern in exclude_patterns:
#         if fnmatch.fnmatch(filepath, pattern):
#             return True
#         if not os.path.isabs(pattern):
#             if fnmatch.fnmatch(filepath, os.path.normpath("*/" + pattern + "/*")):
#                 return True
#             if fnmatch.fnmatch(filepath, os.path.normpath("*/" + pattern)):
#                 return True
#             if fnmatch.fnmatch(filepath, os.path.normpath(pattern + "/*")):
#                 return True
#     return False


# def is_import_all(string):
#     return re.match(r"^import\s+\*\s+as\s+(.+)\s+from\s+(['\"])(.+)\2", string)


# def is_import_default(string):
#     return re.match(r"^import\s+([^ ,{}]+)\s+from\s+(['\"])(.+)\2", string)


# # import React, { useState } from 'react'
# # import React, { useState, useCallback } from 'react'
# def is_import_mixed(string):
#     return re.match(r"^import\s+\w+,\s+\{.+?\}\s+from\s+(['\"])(.+)\1", string)
