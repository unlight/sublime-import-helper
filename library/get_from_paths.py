import os

from .unixify import unixify
from .get_setting import get_setting
from .try_typescript_path import try_typescript_path

# Check if possible insert name multiple ways (different paths)
def get_from_paths(
    item,
    file_name=None,
    typescript_paths=[],
    remove_trailing_index=True,
    import_file_extension="remove",
):
    if item.get("module"):
        from_path = item["module"]
        return [from_path]
    if not file_name:
        file_name = "."
    from_path = os.path.relpath(item["filepath"], os.path.dirname(file_name))
    from_path = unixify(from_path, import_file_extension)
    if from_path[0] != ".":
        from_path = "./" + from_path
    result = [from_path]
    typescript_path = try_typescript_path(item["filepath"], typescript_paths)
    if typescript_path is not None:
        typescript_path = unixify(typescript_path, import_file_extension)
        result.insert(0, typescript_path)
    for i, from_path in enumerate(result):
        if remove_trailing_index and from_path[-6:] == "/index":
            result[i] = from_path[:-6]
    return result
