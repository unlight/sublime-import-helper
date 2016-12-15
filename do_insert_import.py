import sublime
import sublime_plugin
import os
from .utils import unixify, debug

class DoInsertImportCommand(sublime_plugin.TextCommand):
    def run(self, edit, item):
        if (item.get('module')):
            from_path = item['module']
        else:
            file_name = self.view.file_name()
            from_path = os.path.relpath(item['filepath'], os.path.dirname(file_name))
            from_path = unixify(from_path)
            if from_path[0] != '.':
                from_path = './' + from_path
        import_string = "import {0} from '{1}';\n"
        name = item['name']
        if not item['isDefault']:
            name = '{ ' + name + ' }';
        import_string = import_string.format(name, from_path)
        debug('Import string', import_string)
        pos = 0
        self.view.insert(edit, pos, import_string)