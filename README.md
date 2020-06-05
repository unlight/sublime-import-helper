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

#### `insert_position`

Specifies where new import statement should be inserted, at the beginning ('start')
or at the end of imports block ('end').

-   Type: `string`
-   Enum: `['end', 'start']`
-   Default: `end`

#### `from_quote`

What kind of quotes will be used in import statement.

-   Type: `string`
-   Default: `'`

#### `space_around_braces`

Paste space before opening and after closing curly brackets.

-   Type: `boolean`
-   Default: `true`

#### `node_bin`

Sometimes sublime cannot find node executable, if it happens. Set `node_bin` explicitly (e.g. c:/nodejs/node.exe)

-   Type: `string`
-   Default: `` (auto detect)

#### `from_semicolon`

Add semicolon to the end of `import` string.

-   Type: `boolean`
-   Default: `true`

#### `import_path_mapping`

How to apply path mapping (read more about [Module Resolution and Path Mapping](http://www.typescriptlang.org/docs/handbook/module-resolution.html)).  
Disabled by default (`disabled`).  
If `enabled` implementation will try to find first matching alias.

-   Type: `string`
-   Enum: `['disabled', 'enabled']`
-   Default: `disabled`

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

#### `import_no_match_count`

Usually imports are at the top of the file, this settings controls how far countinue scan lines

-   Type: `number`
-   Default: `15`

#### `import_root` (project file only)

Path to your project root folder (not source folder). If not set, `folders[0].path` will be used.

#### `folders[i].path_source` (project file only)

Path to your source. If not set `folders[i].path` will be used.

#### Example of settings in project file:

Example of project file:

```
{
	"import_root": ".",
	"space_around_braces": false,
	"folders": [
		{
			"path": "."
		}
	]
}
```

## FAQ

#### No imports found for...

Or if you see such message in status bar and console:

```
There is no project file, ... will not work without project.
```

You must create project from your working files and folders, you can do it in top menu:  
`Project -> Save project as...`  
Save project file in any place you want.  
Then restart Sublime.

## Development

```python
# sublime.log_input(True); sublime.log_commands(True); sublime.log_result_regex(True)
# sublime.log_input(False); sublime.log_commands(False); sublime.log_result_regex(False)
python3 -m black .
```

## TODO

-   ignore patterns
-   move all commands to main file
-   parse single file
-   handle all selections
-   watch for project file changes
