import sublime
import sys
from unittest import TestCase

import_helper = sys.modules["ImportHelper.import_helper"]
debug = sys.modules["ImportHelper.library.debug"].debug

class TestExample(TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def test_smoke(self):
        self.assertTrue(True)

    def test_hello_world(self):
        self.view.run_command("hello_world")
        first_row = self.getRow(0)

def setText(view, string):
    view.run_command("select_all")
    view.run_command("left_delete")
    view.run_command("insert", {"characters": string})

class TestDebugDisabled(TestCase):
    def test_debug_disabled(self):
        self.assertFalse(sys.modules["ImportHelper.library.debug"].is_debug)

class TestDoInsertImport(TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def getAll(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def test_smoke(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "dinah_widdoes",
                    "name": "Lakia",
                    "isDefault": False,
                }
            },
        )
        first_row = self.getRow(0)
        self.assertEqual("import { Lakia } from './dinah_widdoes';", first_row)

    def test_side_effect_import(self):
        setText(self.view, 'import "rxjs/operators/map"\n')
        self.view.run_command(
            "paste_import",
            {"item": {"filepath": "side/effect", "name": "effect", "isDefault": False}},
        )
        self.assertIn("./side/effect", self.getRow(1))

    def test_paste_import_if_imports_statements_in_the_middle(self):
        setText(self.view, ("\n" * 14) + 'import x from "x"\n')
        self.view.run_command(
            "paste_import",
            {"item": {"filepath": "filepath", "name": "name", "isDefault": False}},
        )
        first_row = self.getRow(0)
        self.assertNotIn("./filepath", first_row)
        self.assertNotIn("name", first_row)

    def test_add_specifier_to_default_import(self):
        setText(self.view, "import React from 'react'\n")
        self.view.run_command(
            "paste_import",
            {"item": {"name": "useCallback", "module": "react", "isDefault": False}},
        )
        self.assertIn("import React, { useCallback } from 'react", self.getRow(0))

    def test_add_specifier_to_mixed_import(self):
        setText(self.view, "import React, { useCallback } from 'react'\n")
        self.view.run_command(
            "paste_import",
            {"item": {"name": "useState", "module": "react", "isDefault": False}},
        )
        self.assertIn(
            "import React, { useCallback, useState } from 'react", self.getRow(0)
        )

    # These tests shows additional popup
    def test_typescript_paths(self):
        typescript_paths = [
            {
                "path_to": "@Libs/*",
                "path_value": "./test_playground/lib/*",
                "base_dir": "/base_dir",
            },
        ]
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "/base_dir/test_playground/lib/a/b/c.ts",
                    "name": "name",
                    "isDefault": False,
                },
                "typescript_paths": typescript_paths,
                "test_selected_index": 0,
            },
        )
        self.assertIn("@Libs/a/b/c", self.getRow(0))

    def test_typescript_paths_2(self):
        typescript_paths = [
            {
                "path_to": "@z_component",
                "path_value": "./app/components/z.ts",
                "base_dir": "/base_dir",
            },
        ]
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "/base_dir/app/components/z.ts",
                    "name": "zoo",
                    "isDefault": False,
                },
                "typescript_paths": typescript_paths,
                "test_selected_index": 0,
            },
        )
        self.assertIn("import { zoo } from '@z_component'", self.getRow(0))

    def test_typescript_paths_3(self):
        typescript_paths = [
            {
                "path_to": "@components",
                "path_value": "./app/components",
                "base_dir": "/base_dir",
            },
        ]
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "/base_dir/app/components/index.ts",
                    "name": "koo",
                    "isDefault": False,
                },
                "typescript_paths": typescript_paths,
                "test_selected_index": 0,
            },
        )
        self.assertIn("import { koo } from '@components'", self.getRow(0))

    def test_remove_importpath_index(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "./component/x/index",
                    "name": "x1",
                    "isDefault": False,
                }
            },
        )
        self.assertIn("import { x1 } from './component/x'", self.getRow(0))
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "./component/x/index",
                    "name": "x2",
                    "isDefault": False,
                }
            },
        )
        self.assertIn("import { x1, x2 } from './component/x'", self.getRow(0))

    def test_paste_import_module(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "module": "@angular/core",
                    "isDefault": False,
                    "name": "Inject",
                }
            },
        )
        self.assertIn("import { Inject } from '@angular/core'", self.getRow(0))

    def test_paste_import_no_semicolon(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "mod",
                    "name": "x",
                    "isDefault": True,
                },
                "settings": {"no_semicolon": True},
            },
        )
        self.assertEqual("import x from './mod'", self.getRow(0))

    def test_paste_import_no_spaces_in_braces(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {
                    "filepath": "file",
                    "name": "a",
                    "isDefault": False,
                },
                "settings": {"insert_space_in_braces": False, "no_semicolon": True},
            },
        )
        self.assertEqual("import {a} from './file'", self.getRow(0))


class TestInitializeSetup(TestCase):
    def setUp(self):
        self.window = sublime.active_window()
        self.window.run_command("initialize_setup")

    def test_check_node_modules(self):
        yield 5000
        self.assertNotEqual(len(import_helper.NODE_MODULES), 0)

    def test_check_source_modules(self):
        yield 1000
        self.assertNotEqual(len(import_helper.SOURCE_MODULES), 0)


class TestPasteImport(TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def getRow(self, row):
        return self.view.substr(self.view.line(self.view.text_point(row, 0)))

    def getAll(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def test_paste_import_extension_remove(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {"filepath": "file.tsx", "name": "a"},
                "settings": {},
            },
        )
        self.assertEqual("import { a } from './file';", self.getRow(0))

    def test_paste_import_extension_js(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {"filepath": "file.tsx", "name": "a"},
                "settings": {"import_file_extension": "js"},
            },
        )
        self.assertEqual("import { a } from './file.js';", self.getRow(0))

    def test_paste_import_extension_js_should_not_remove_index(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {"filepath": "./x/index.tsx", "name": "x"},
                "settings": {
                    "import_file_extension": "js",
                    "remove_trailing_index": True,
                },
            },
        )
        self.assertEqual("import { x } from './x/index.js';", self.getRow(0))

    def test_paste_import_extension_as_is(self):
        setText(self.view, "")
        self.view.run_command(
            "paste_import",
            {
                "item": {"filepath": "./a.jsx", "name": "b"},
                "settings": {
                    "import_file_extension": "as_is",
                    "remove_trailing_index": True,
                },
            },
        )
        self.assertEqual("import { b } from './a.jsx';", self.getRow(0))