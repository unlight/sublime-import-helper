import sublime
import sublime_plugin
import os
import re
from .utils import debug, run_command_async
from .import_helper import PROJECT_NAME, get_import_root

# view.run_command('remove_unused')
class RemoveUnusedCommand(sublime_plugin.TextCommand):
    
    def run(self, edit):
        file_name = self.view.file_name()
        if file_name is None or self.view.is_dirty():
            sublime.status_message('File must be saved')
            return
        data = {'file_name': self.view.file_name(), 'cwd': get_import_root()}
        run_command_async('remove_unused', data, self.callback)

    def callback(self, err, result):
        if (err is not None):
            debug(err, force=True)
            sublime.error_message("\n".join([
                PROJECT_NAME,
                "Error while running typescript compiler:",
                str(err)
            ]))
            return
        if len(result) == 0:
            sublime.status_message('Nothing to remove')
        self.view.run_command('edit_remove_unsed_imports', args=({'data': result}))

# view.run_command('edit_remove_unsed_imports', args=({'data': {"1":[{"line":1,"pos":22,"name":"f"}]}}))
class EditRemoveUnsedImports(sublime_plugin.TextCommand):

    def run(self, edit, data):
        empty_lines = []
        for line, infoList in data.items():
            line_index = int(line) - 1
            line_region = self.view.full_line(self.view.text_point(line_index, 0))
            line_contents = self.view.substr(line_region)
            match = re.search(r"^import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            if match is None:
                continue
            # import_names = match.group(1)
            for info in infoList:
                name = info['name']
                line_contents = re.sub(r"((,\s*)(\w+\s+as\s+)?\b" + name + r"\b|(\w+\s+as\s+)?\b" + name + r"\b(,\s*)|(\w+\s+as\s+)?\b" + name + r"\b)", '', line_contents, 1)
            remove_line = re.search(r"import\s+{\s*}", line_contents) is not None
            if remove_line:
                # debug("Line has to be removed", self.view.substr(self.view.line(self.view.text_point(line_index, 0))))
                empty_lines.append(line_index)
                continue
            self.view.replace(edit, line_region, line_contents)
        # remove empty lines if any
        if len(empty_lines) > 0:
            empty_lines.sort()
            for n, line_index in enumerate(empty_lines):
                line_region = self.view.full_line(self.view.text_point(line_index - n, 0))
                # debug("Removing line", self.view.substr(line_region))
                self.view.erase(edit, line_region)
