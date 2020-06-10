# sublime-import-helper

A Sublime Text Plugin that helps you to import your modules.

## Supported Languages

-   TypeScript
-   JavaScript (ES2015)

## Requirements

-   Node.JS 10.0+

## Installation

#### [PackageControl](https://packagecontrol.io/packages/ImportHelper)

-   Select `Package Control: Install Package` from command palette
-   Select `ImportHelper`

#### Manual Installation

You can install `sublime-import-helper` manually using git by running the following command
within sublime packages directory (Preferences > Browse Packages):

```
git clone https://github.com/unlight/sublime-import-helper ImportHelper
```

#### Install Old version

Check https://github.com/unlight/sublime-import-helper/releases page,
dowload source code archive, unzip to `Data/Packages/ImportHelper`.

Or you can use git, see like in manual installation:

```sh
git clone https://github.com/unlight/sublime-import-helper ImportHelper
cd ImportHelper
git checkout -f v2.3.2
```

## Usage

#### Initialize / Setup / Update modules

-   Restart plugin - update node_modules, source modules

#### Insert import

-   Set cursor or select word
-   Press `ctrl+alt+i`, or select the command from command palette

#### List imports

-   Press `alt+i, alt+l`, or select the command from command palette

#### Update source modules

-   Press `alt+i, alt+s`, or select the command from command palette

#### Import from clipboard

-   Copy text to clipboard `ctrl+c`
-   Press `alt+i, alt+k`, or select the command from command palette

## Screenshots

![](https://raw.githubusercontent.com/unlight/sublime-import-helper/master/screenshots/insert-import.gif)

## Settings

There are some several configuration settings. Open plugin settings file by opening in menu:  
Preferences -> Package Settings -> Import Helper  
Also, there are some optional project specific settings.  
The precedence of getting of value of setting is following:

1. Project file
2. Plugin file settings
3. Default settings

#### `from_quote`

What kind of quotes will be used in import statement.

-   Type: `string`
-   Default: `'`

#### `node_bin`

Sometimes sublime cannot find node executable, if it happens. Set `node_bin` explicitly (e.g. c:/nodejs/node.exe)

-   Type: `string`
-   Default: 'node' (auto detect)

#### `import_path_mapping`

How to apply path mapping (read more about [Module Resolution and Path Mapping](http://www.typescriptlang.org/docs/handbook/module-resolution.html)).

If `enabled` implementation will try to find first matching alias.

-   Type: `string`
-   Enum: `['disabled', 'enabled']`
-   Default: `enabled`

#### `autocomplete_export_names`

Show all possible export names from sources and node modules in autocomplete menu.

-   Type: `boolean`
-   Default: `true`

#### `autocomplete_auto_import`

Automatically add import statement if export name was selected from autocomplete menu (Ctrl + Space).  
Requires `autocomplete_export_names: true`.

-   Type: `boolean`
-   Default: `false`

#### `remove_trailing_index`

Remove index suffix ending in file path

-   Type: `boolean`
-   Default: `true`

#### `import_root` (project file only)

Path to your project root folder (not source folder). If not set,
tries automatically detect. For single souce folder `folders[0].path` will be used,
for serveral source folders common path will be used.

#### Example of settings in project file:

Example of project file:

```
{
	"import_root": ".",
	"from_quote": "'",
	"folders": [
		{
			"path": "."
		}
	]
}
```

## Notes for `No imports found for ...` message

Looks like you do not have opened folders in current Sublime window.

It is recommended to create project from your working files and folders, you can do it in top menu:  
`Project -> Save project as...`  
Save project file in any place you want.  
Then restart Sublime.

Currently, it is not posssible to detect when project was switched (Project -> Quick Switch Project),
in this case you need manually re-initialize plugin:  
Select `Import Helper: Initialize / Setup / Update modules` from command palette

## Dev Notes

```python
sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)
python3 -m black .
```

## TODO

-   run node check version on startup
-   limit to 100 panel items
-   multiple source folders (import_root setting canbe removed)
-   parse single file
-   handle all selections
-   watch for project file changes
