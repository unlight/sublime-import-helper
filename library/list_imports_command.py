from functools import partial

from .get_import_root import get_import_root
from .panel_items import get_panel_item
from .debug import debug


def list_imports_command(
    view, import_root=get_import_root(), entry_modules=[], typescript_paths=[]
):
    # todo: to new func
    match_items = []
    panel_items = []
    for item in entry_modules:
        panel_item = get_panel_item(import_root, item)
        panel_items.append(panel_item)
        match_items.append(item)

    def on_select(index):
        if index == -1:
            return
        selected_item = match_items[index]
        debug("list_imports_command:on_select", selected_item)
        view.run_command(
            "paste_import",
            {"item": selected_item, "typescript_paths": typescript_paths},
        )

    view.window().show_quick_panel(panel_items, on_select)
