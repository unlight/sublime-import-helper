import re
from .get_setting import get_setting

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
