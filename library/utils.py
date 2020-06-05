import sublime
import os
import sys
import platform
import subprocess
import threading
import socket
import fnmatch
import time
import re

from .unixify import unixify
from .get_setting import get_setting
from .debug import debug


def norm_path(base, to):
    return os.path.normpath(os.path.join(os.path.dirname(base), to))


def get_time():
    return time.time()


def is_excluded_file(filepath, exclude_patterns):
    if exclude_patterns is None or len(exclude_patterns) == 0:
        return False
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(filepath, pattern):
            return True
        if not os.path.isabs(pattern):
            if fnmatch.fnmatch(filepath, os.path.normpath("*/" + pattern + "/*")):
                return True
            if fnmatch.fnmatch(filepath, os.path.normpath("*/" + pattern)):
                return True
            if fnmatch.fnmatch(filepath, os.path.normpath(pattern + "/*")):
                return True
    return False


def is_import_all(string):
    return re.match(r"^import\s+\*\s+as\s+(.+)\s+from\s+(['\"])(.+)\2", string)


def is_import_default(string):
    return re.match(r"^import\s+([^ ,{}]+)\s+from\s+(['\"])(.+)\2", string)


# import React, { useState } from 'react'
# import React, { useState, useCallback } from 'react'
def is_import_mixed(string):
    return re.match(r"^import\s+\w+,\s+\{.+?\}\s+from\s+(['\"])(.+)\1", string)


def try_typescript_path(filepath, typescript_paths):
    import_path_mapping = get_setting("import_path_mapping", "none")
    if import_path_mapping == "enabled":
        (drive, filepath) = os.path.splitdrive(filepath)
        filepath = filepath.replace("\\", "/")
        # debug("filepath", filepath)
        for ts_path in typescript_paths:
            base_dir = ts_path["base_dir"]
            path_value = ts_path["path_value"]
            path_to = ts_path["path_to"]
            (drive, test_path) = os.path.splitdrive(
                os.path.normpath(os.path.join(base_dir, path_value)).replace("\\", "/")
            )
            # debug("test_path", test_path)
            # "@app/*" :["app/*"]
            if test_path[-2:] == "/*" and path_to[-2:] == "/*":
                test_path = test_path[0:-2]
                if filepath.startswith(test_path):
                    test_path = path_to[0:-2] + filepath[len(test_path) :]
                    return test_path
            # "@lib": ["app/lib"]
            if filepath == test_path or filepath in [
                test_path + "/index.ts",
                test_path + "/index.tsx",
                test_path + "/index.js",
                test_path + "/index.jsx",
            ]:
                return path_to
    return None


def wrap_imports(imports):
    start = "{"
    end = "}"
    if get_setting("space_around_braces", True):
        start = start + " "
        end = " " + end
    return start + ", ".join(imports) + end


def get_import_line_info(view, from_path):
    row = 0
    import_row = -1  # initial value -1 not found
    last_row = view.rowcol(view.size())[0]
    import_no_match_count = get_setting("import_no_match_count", 15)
    no_match_count = 0
    last_import_row = -1
    while row <= last_row:
        line_region = view.full_line(view.text_point(row, 0))
        line_contents = view.substr(line_region)
        match = re.search(r"^import\s+((.+)\s+from\s+)?(['\"])(.+)\3", line_contents)
        if match:
            last_import_row = row
            no_match_count = 0
            if match.group(4) == from_path:
                import_row = row
                break
        else:
            no_match_count = no_match_count + 1
        # Break loop if cannot find lines with import
        if no_match_count >= import_no_match_count:
            break
        # Go to next line
        row = row + 1
    imports = []
    if import_row != -1:
        for m in re.finditer(r"(\w+(\s+as\s+\w+)?)", match.group(2)):
            imports.append(m.group(1))
    return {
        "import_row": import_row,
        "imports": imports,
        "from_path": from_path,
        "last_import_row": last_import_row,
        "line_contents": line_contents,
    }
