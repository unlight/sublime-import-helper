import sublime
import sublime_plugin
import os
import re
from .utils import unixify, debug

# view.run_command('do_insert_import', args=({'item': {'filepath': 'xxx', 'name': 'aaa', 'isDefault': False}}))
class DoInsertImportCommand(sublime_plugin.TextCommand):
    
    def run(self, edit, item):
        view = self.view
        if (item.get('module')):
            from_path = item['module']
        else:
            file_name = self.view.file_name()
            from_path = os.path.relpath(item['filepath'], os.path.dirname(file_name))
            from_path = unixify(from_path)
            if from_path[0] != '.':
                from_path = './' + from_path
        import_string = "import {0} from '{1}';\n"
        find_line_result = self.find_line(from_path)
        name = item['name']
        if not find_line_result:
            if not item['isDefault']:
                name = '{ ' + name + ' }';
            import_string = import_string.format(name, from_path)
            debug('Import string', import_string)
            pos = 0
            view.insert(edit, pos, import_string)
        else:
            (imports, region) = find_line_result
            try: imports.remove(name)
            except: pass
            imports.append(name)
            name = '{ ' + ', '.join(imports) + ' }'
            import_string = import_string.format(name, from_path)
            debug('Import string', import_string)
            view.replace(edit, region, import_string)
    
    def find_line(self, from_path):
        view = self.view
        row = -1
        found = False
        while row < 255:
            row = row + 1
            point = view.text_point(row, 0)
            line_region = view.full_line(point)
            line_contents = view.substr(line_region)
            # match = re.search(r"^import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            match = re.search(r"import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            if match:
                match_from = match.group(3)
                if from_path == match_from:
                    found = True
                    break
        if not found:
            debug('Do insert command (find_line row)', row)
            return None
        dirty_names = match.group(1)
        # TODO: Fix fails on defalt import.
        imports = re.findall(r"{?(\w+)}?", dirty_names)
        return (imports, line_region)
