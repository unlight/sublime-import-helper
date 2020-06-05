import os
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
