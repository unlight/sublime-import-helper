import os
from .unixify import unixify

# Prepare string to show in window's quick panel.
def get_panel_item(root, item):
    module = item.get("module")
    name = item.get("name")
    if module is not None:
        if module == name and item.get("isDefault") == True:
            return module + "/default"
        return module + "/" + name
    filepath = os.path.normpath(item["filepath"])[len(root) + 1 :]
    return unixify(filepath) + "/" + name
