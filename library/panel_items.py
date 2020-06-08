import os
from .unixify import unixify
from .get_import_root import get_import_root


def panel_items(name=None, entry_modules=[], import_root=get_import_root()):
    result = []
    matches = []
    slice_length = len(import_root) + 1
    for item in entry_modules:
        if name is not None and item.get("name") != name:
            continue
        panel_item = get_panel_item(item, slice_length)
        result.append(panel_item)
        matches.append(item)
    return (result, matches)


# Prepare string to show in window's quick panel.
def get_panel_item(item, slice_length):
    module = item.get("module")
    name = item.get("name")
    if module is not None:
        if module == name and item.get("isDefault") == True:
            return module + "/default"
        return module + "/" + name
    filepath = os.path.normpath(item["filepath"])[slice_length:]
    return unixify(filepath) + "/" + name
