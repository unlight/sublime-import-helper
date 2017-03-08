sublime-import-helper
=====================
A Sublime Text Plugin that helps you to import your modules.

Supported Languages
---
* TypeScript
* JavaScript (ES2015)

## Requirements
* Node.JS 6.0+

Installation
---
#### [PackageControl](https://packagecontrol.io/packages/ImportHelper)
* Select `Package Control: Install Package` from command palette
* Select `ImportHelper`

#### Manual Installation
You can install `sublime-import-helper` manually using git by running the following command
within sublime packages directory (Preferences > Browse Packages):
```
git clone https://github.com/unlight/sublime-import-helper ImportHelper
```

Usage
---
#### Insert import
* Set cursor or select word
* Press `ctrl+alt+i`, or select the command from command palette

#### List imports
* Press `alt+i, alt+l`, or select the command from command palette

#### Update imports
* Select the command from command palette

#### Import from clipboard
* Copy text to clipboard `ctrl+c`
* Press `alt+i, alt+k`, or select the command from command palette

Screenshots
---
![](https://raw.githubusercontent.com/unlight/sublime-import-helper/master/screenshots/insert-import.gif)

Project Settings
---
#### `import_root`
Path to your project root folder (not source folder). If not set, `folders[0].path` will be used.

#### `folders[i].path_source`
Path to your source. If not set `folders[i].path` will be used.

Plugin Settings
---
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

CHANGELOG
---
| Version | Date        | Description                               |
|:--------|:------------|:------------------------------------------|
| 1.1.1   | 09 Mar 2017 | Respect exclude_patterns project settings |
| 1.1.0   | 25 Feb 2017 | Auto update imports when new file saved   |
|         |             | Unit tests, bug fixing                    |
|         |             | Parse inner modules                       |
| 1.0.10  | 30 Jan 2017 | Fixed errors when broken package.json     |
| 1.0.8   | 24 Jan 2017 | Added .no-sublime-package                 |
| 1.0.7   | 21 Jan 2017 | Fixed #10 incorrect adding to `import as` |
| 1.0.6   | 10 Jan 2017 | Updated esm-exports modules to 0.3.2      |
| 1.0.5   | 10 Jan 2017 | Updated esm-exports modules to 0.3.1      |
| 1.0.3   | 26 Dec 2016 | Setting `space_around_braces`             |
| 1.0.1   | 19 Dec 2016 | Fixed loading settings bug                |
| 1.0.0   | 18 Dec 2016 | First release                             |

TODO
---
* parse single file
* Handle all selections
* watch for project file changes
* update imports on adding file