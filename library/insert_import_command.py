import re
import sublime
from functools import partial

from .debug import debug
from .get_import_root import get_import_root
from .panel_items import panel_items


def insert_import_command(
    view, point, notify, entry_modules, import_root, name=None, typescript_paths=[],
):
    if not name:
        name = get_name_candidate(view, point)
    name = re.sub(r"[^\w\-\@\/]", "", name)
    if not name:
        return

    debug("insert_import: trying to import", "`{0}`".format(name))

    (items, matches) = panel_items(
        name=name, entry_modules=entry_modules, import_root=import_root
    )

    if len(items) == 0 and notify:
        view.show_popup("No imports found for `<strong>{0}</strong>`".format(name))
        return
    if len(items) == 1:
        item = matches[0]
        view.run_command(
            "paste_import", {"item": item, "typescript_paths": typescript_paths}
        )
        return

    def on_select(index):
        if index == -1:
            return
        selected_item = matches[index]
        debug("insert_import: on_select", selected_item)
        view.run_command(
            "paste_import",
            {"item": selected_item, "typescript_paths": typescript_paths},
        )

    view.window().show_quick_panel(items, on_select)


def get_name_candidate(view, point):
    point_region = view.sel()[0]
    if point is not None:
        point_region = sublime.Region(point, point)
    name = view.substr(point_region).strip()
    if not name:
        cursor_region = view.expand_by_class(
            point_region,
            sublime.CLASS_WORD_START
            | sublime.CLASS_LINE_START
            | sublime.CLASS_PUNCTUATION_START
            | sublime.CLASS_WORD_END
            | sublime.CLASS_PUNCTUATION_END
            | sublime.CLASS_LINE_END,
        )
        name = view.substr(cursor_region)
    return name
