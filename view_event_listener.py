import sublime_plugin
from .import_helper import SOURCE_MODULES, NODE_MODULES
from .library.get_setting import get_setting
from .library.query_completions_modules import query_completions_modules
from .library.utils import get_time


class ImportHelperViewEventListener(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        super().__init__(view)
        self.completions_info = {"time": -1, "result": [], "prefix": ""}
        self.in_auto_complete = False
        self.autocomplete_point = 0
        self.autocomplete_export_names = get_setting("autocomplete_export_names", True)
        self.autocomplete_auto_import = get_setting("autocomplete_auto_import", False)

    def on_query_completions(self, prefix, locations):
        if not self.autocomplete_export_names or not (
            len(prefix) > 0
            and self.view.match_selector(
                self.autocomplete_point, "source.ts, source.tsx, source.js, source.jsx"
            )
        ):
            return []
        self.autocomplete_point = locations[0]
        if (
            get_time() > self.completions_info["time"] + 1
            or prefix != self.completions_info["prefix"]
        ):
            self.completions_info["time"] = get_time()
            self.completions_info["prefix"] = prefix
            self.completions_info["result"] = query_completions_modules(
                prefix, SOURCE_MODULES, NODE_MODULES
            )
        return self.completions_info["result"]

    def on_post_text_command(self, command_name, args):
        if not (self.autocomplete_auto_import and self.autocomplete_export_names):
            return
        if self.in_auto_complete and command_name in [
            "insert_best_completion",
            "insert_dimensions",
        ]:
            self.in_auto_complete = False
            self.view.run_command(
                "insert_import",
                args=({"point": self.autocomplete_point - 1, "notify": False}),
            )
        elif command_name in [
            "auto_complete",
            "replace_completion_with_next_completion",
            "replace_completion_with_auto_complete",
        ]:
            self.in_auto_complete = True
        elif command_name == "hide_auto_complete":
            self.in_auto_complete = False

    def on_activated(self):
        self.in_auto_complete = False
