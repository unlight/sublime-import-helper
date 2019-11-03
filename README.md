# sublime-import-helper
A Sublime Text Plugin that helps you to import your modules.

## Supported Languages
* TypeScript
* JavaScript (ES2015)

## Requirements
* Node.JS 6.0+

## Installation
#### [PackageControl](https://packagecontrol.io/packages/ImportHelper)
* Select `Package Control: Install Package` from command palette
* Select `ImportHelper`

#### Manual Installation
You can install `sublime-import-helper` manually using git by running the following command
within sublime packages directory (Preferences > Browse Packages):
```
git clone https://github.com/unlight/sublime-import-helper ImportHelper
```

## Usage
#### Initialize / Setup / Update modules
* Restart plugin - update node_modules, source modules

#### Insert import
* Set cursor or select word
* Press `ctrl+alt+i`, or select the command from command palette

#### List imports
* Press `alt+i, alt+l`, or select the command from command palette

#### Update source modules
* Press `alt+i, alt+s`, or select the command from command palette

#### Import from clipboard
* Copy text to clipboard `ctrl+c`
* Press `alt+i, alt+k`, or select the command from command palette

#### Remove unused imports (TypeScript only)
* Press `alt+i, alt+u`, or select the command from command palette

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
- Type: `string`
- Enum: `['end', 'start']`
- Default: `end`

#### `from_quote`
What kind of quotes will be used in import statement.
- Type: `string`
- Default: `'`

#### `space_around_braces`
Paste space before opening and after closing curly brackets.
- Type: `boolean`
- Default: `true`

#### `node_bin`
Sometimes sublime cannot find node executable, if it happens. Set `node_bin` explicitly (e.g. c:/nodejs/node.exe)
- Type: `string`
- Default: `` (auto detect)

#### `from_semicolon`
Add semicolon to the end of `import` string. 
- Type: `boolean`
- Default: `true`

#### `import_path_mapping`
How to apply path mapping (read more about [Module Resolution and Path Mapping](http://www.typescriptlang.org/docs/handbook/module-resolution.html)).  
Disabled by default (`disabled`).  
If `enabled` implementation will try to find first matching alias.  
- Type: `string`  
- Enum: `['disabled', 'enabled']`  
- Default: `disabled`  

#### `autocomplete_export_names`
Show all possible export names from sources and node modules in autocomplete menu.  
- Type: `boolean`  
- Default: `true`

#### `autocomplete_auto_import`
Automatically add import statement if export name was selected from autocomplete menu (Ctrl + Space).  
Requires `autocomplete_export_names: true`.  
- Type: `boolean`  
- Default: `false`

#### `remove_trailing_index`
Remove index suffix ending in file path  
- Type: `boolean`  
- Default: `true`  

#### `import_no_match_count`
Usually imports are at the top of the file, this settings controls how far countinue scan lines  
- Type: `number`  
- Default: `15`  

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

## CHANGELOG
| Version | Date        | Description                                                                                                     |
|:--------|:------------|:----------------------------------------------------------------------------------------------------------------|
| 2.3.1   | 03 Nov 2019 | Fixed [#71](https://github.com/unlight/sublime-import-helper/issues/71)                                                                                    |
| 2.3.0   | 14 Sep 2019 | Minor fixes, progress status                                                                                    |
| 2.2.1   | 15 Jun 2019 | Minor fixes                                                                                                     |
| 2.2.0   | 22 May 2019 | Support passing file / folder exclude options [#64](https://github.com/unlight/sublime-import-helper/issues/64) |
| 2.1.0   | 31 Mar 2019 | Refactoring, updated esm-exports, allow import default, fixed exclude logic                                     |
| 2.0.5   | 22 Dec 2018 | Fixed [#61](https://github.com/unlight/sublime-import-helper/issues/61)                                         |
| 2.0.4   | 08 Dec 2018 | Fixed #62 (remove unsed imports with dollar sign                                                                |
| 2.0.3   | 10 Nov 2018 | Alllow to select import path (typescript paths)                                                                 |
| 2.0.2   | 13 Oct 2018 | Remove trailing index in import path [#59](https://github.com/unlight/sublime-import-helper/issues/59)          |
|         |             | Null reference [#60](https://github.com/unlight/sublime-import-helper/issues/60)                                |
| 2.0.1   | 13 Aug 2018 | Added key bind to update source modules [#58](https://github.com/unlight/sublime-import-helper/issues/58)       |
| 2.0.0   | 20 Apr 2018 | Path mapping [#54](https://github.com/unlight/sublime-import-helper/issues/54)                                  |
|         |             | Autocomplete support [#57](https://github.com/unlight/sublime-import-helper/issues/57)                          |
| 1.8.2   | 14 Apr 2018 | Fixed [#56](https://github.com/unlight/sublime-import-helper/issues/56)                                         |
| 1.8.1   | 22 Feb 2018 | Fixed [#51](https://github.com/unlight/sublime-import-helper/issues/51)                                         |
| 1.8.0   | 22 Feb 2018 | Fixed [#50](https://github.com/unlight/sublime-import-helper/issues/50)                                         |
| 1.7.6   | 12 Dec 2017 | Fixed [#47](https://github.com/unlight/sublime-import-helper/issues/47)                                         |
| 1.7.5   | 11 Dec 2017 | Added `from_semicolon` setting                                                                                  |
| 1.7.4   | 30 Nov 2017 | Delayed initialization                                                                                          |
| 1.7.3   | 30 Nov 2017 | `node_bin` setting to explicitly set path to node binary                                                        |
| 1.7.1   | 29 Nov 2017 | Try to find node executable                                                                                     |
| 1.7.0   | 22 Nov 2017 | Updated `esm-exports` to 2.0.0                                                                                  |
|         |             | Added shell true #43                                                                                            |
| 1.6.4   | 03 Nov 2017 | Updated `esm-exports` to v0.8.5                                                                                 |
| 1.6.3   | 20 Oct 2017 | Fixed #42 settings does not work                                                                                |
| 1.6.2   | 18 Oct 2017 | Fix for empty projects                                                                                          |
| 1.6.0   | 06 Oct 2017 | New feature remove unused imports                                                                               |
| 1.5.0   | 24 Jun 2017 | Added update source modules command                                                                             |
| 1.4.1   | 03 May 2017 | Import tsx/jsx without extension                                                                                |
| 1.4.0   | 29 Mar 2017 | Settings per project                                                                                            |
| 1.3.0   | 23 Mar 2017 | Prevent fail while parse link to not existing directory                                                         |
| 1.1.1   | 09 Mar 2017 | Respect exclude_patterns project settings                                                                       |
| 1.1.0   | 25 Feb 2017 | Auto update imports when new file saved                                                                         |
|         |             | Unit tests, bug fixing                                                                                          |
|         |             | Parse inner modules                                                                                             |
| 1.0.10  | 30 Jan 2017 | Fixed errors when broken package.json                                                                           |
| 1.0.8   | 24 Jan 2017 | Added .no-sublime-package                                                                                       |
| 1.0.7   | 21 Jan 2017 | Fixed #10 incorrect adding to `import as`                                                                       |
| 1.0.6   | 10 Jan 2017 | Updated esm-exports modules to 0.3.2                                                                            |
| 1.0.5   | 10 Jan 2017 | Updated esm-exports modules to 0.3.1                                                                            |
| 1.0.3   | 26 Dec 2016 | Setting `space_around_braces`                                                                                   |
| 1.0.1   | 19 Dec 2016 | Fixed loading settings bug                                                                                      |
| 1.0.0   | 18 Dec 2016 | First release                                                                                                   |

## TODO
* parse single file
* handle all selections
* watch for project file changes
