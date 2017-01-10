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
#### PackageControl
Not yet.

#### Manual Installation
You can install `sublime-import-helper` manually using git by running the following command
within sublime packages directory (Preferences > Browse Packages):
```
git clone https://github.com/unlight/sublime-import-helper ImportHelper
```

Usage
---
#### Insert import
1. Set cursor or select word
2. Press `ctrl+alt+i`, or select the command from command palette

#### List imports
1. Press `alt+i, alt+l`, or select the command from command palette

#### Update imports
1. Select the command from command palette

#### Import from clipboard
1. Copy text to clipboard `ctrl+c`
2. Press `alt+i, alt+k`, or select the command from command palette

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
| Version | Date        | Description                          |
|:--------|:------------|:-------------------------------------|
| 1.0.5   | 10 Jan 2017 | Updated esm-exports modules to 0.3.1 |
| 1.0.3   | 26 Dec 2016 | Setting `space_around_braces`        |
| 1.0.1   | 19 Dec 2016 | Fixed loading settings bug           |
| 1.0.0   | 18 Dec 2016 | First release                        |

TODO
---
* Handle all selections
* settings: import_max_length
* TODO in *.py files
* watch for project file changes
* update imports on adding file