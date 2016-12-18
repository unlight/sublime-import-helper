import sublime_plugin
import os
import re
from .utils import unixify, debug

# TODO: Get from settings.
insert_position = "end"

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

        name = item['name']
        import_info = self.get_import_info(from_path)
        if not import_info.get('line_region') or item['isDefault']:
            if not item['isDefault']:
                name = '{ ' + name + ' }'
            import_string = import_string.format(name, from_path)
            debug('Import string', import_string)
            pos = 0
            if "end" == insert_position:
                pos = view.text_point(import_info['last_import_row'] + 1, 0)
            view.insert(edit, pos, import_string)
        else:
            imports = import_info['imports']
            line_region = import_info['line_region']
            try: imports.remove(name)
            except: pass
            imports.append(name)
            name = '{ ' + ', '.join(imports) + ' }'
            import_string = import_string.format(name, from_path)
            debug('Import string', import_string)
            view.replace(edit, line_region, import_string)

    def get_import_info(self, from_path):
        view = self.view
        row = -1
        found = False
        last_row = view.rowcol(view.size())[0]
        last_import_row = row
        while row <= last_row:
            row = row + 1
            line_region = view.full_line(view.text_point(row, 0))
            line_contents = view.substr(line_region)
            # match = re.search(r"^import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            # TODO: Use expr above.
            match = re.search(r"import\s+(.+)\s+from\s+(['\"])(.+)\2", line_contents)
            if match:
                last_import_row = row
                if match.group(3) == from_path:
                    found = True
                    break
        if not found:
            return {'last_import_row': last_import_row}
        dirty_names = match.group(1)
        if dirty_names[0] != '{' and dirty_names[-1] != '}':
            # Found unexpected statement.
            return {'last_import_row': last_import_row}
        else:
            imports = re.findall(r"(\w+)", dirty_names)
            return {'imports': imports, 'line_region': line_region, 'last_import_row': last_import_row}
