import sublime
import sys
from unittest import TestCase

import_helper = sys.modules["ImportHelper.import_helper"]
debug = sys.modules["ImportHelper.library.debug"].debug
unixify = sys.modules["ImportHelper.library.unixify"].unixify
get_import_root = sys.modules["ImportHelper.library.get_import_root"].get_import_root
get_setting = sys.modules["ImportHelper.library.get_setting"].get_setting
find_executable = sys.modules["ImportHelper.library.find_executable"].find_executable
get_panel_item = sys.modules["ImportHelper.library.get_panel_item"].get_panel_item
get_exclude_patterns = sys.modules[
    "ImportHelper.library.get_exclude_patterns"
].get_exclude_patterns
query_completions_modules = sys.modules[
    "ImportHelper.library.query_completions_modules"
].query_completions_modules


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
        self.assertIn("import { Lakia } from './dinah_widdoes'", first_row)

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


class TestUtilFunctions(TestCase):
    def test_unixify(self):
        testFile = "\\local\\some\\file"
        self.assertEqual(unixify(testFile), "/local/some/file")

    def test_unixify_ts(self):
        self.assertEqual(unixify("some\\file.ts"), "some/file")

    def test_unixify_tsx(self):
        self.assertEqual(unixify("d/file.tsx"), "d/file")

    def test_unixify_js(self):
        self.assertEqual(unixify("some\\file.js"), "some/file")

    def test_get_setting(self):
        self.assertEqual(get_setting("from_quote", None), "'")
        self.assertEqual(get_setting("unknown", "default_value"), "default_value")

    def test_find_executable(self):
        result = find_executable("node")
        self.assertNotEqual("node", result)

    # def test_get_import_root(self):
    #       todo: try set_project_data
    #     result = get_import_root()
    #     self.assertTrue("ImportHelper" in result)

    def test_query_completions_modules(self):
        source_modules = [
            {"name": "good", "filepath": "/usr/home/good"},
            {"name": "ugly", "filepath": "/usr/home/ugly"},
        ]
        node_modules = [{"name": "Chicky", "module": "chicken"}]
        result = query_completions_modules("goo", source_modules, node_modules)
        self.assertListEqual(result, [["good\tsource_modules", "good"]])
        result = query_completions_modules("Chic", source_modules, node_modules)
        self.assertListEqual(result, [["Chicky\tnode_modules/chicken", "Chicky"]])

    def test_get_exclude_patterns_fault_tollerance(self):
        result = get_exclude_patterns({"folders": {}})
        self.assertDictEqual(result, {})


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

    def test_get_import_block(self):
        pass


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
