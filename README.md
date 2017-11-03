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

#### Update source modules
* Select the command from command palette

#### Update imports
* Select the command from command palette

#### Import from clipboard
* Copy text to clipboard `ctrl+c`
* Press `alt+i, alt+k`, or select the command from command palette

#### Remove unused imports (TypeScript only)
* Press `alt+i, alt+u`, or select the command from command palette

Screenshots
---
![](https://raw.githubusercontent.com/unlight/sublime-import-helper/master/screenshots/insert-import.gif)

Settings
---
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

#### `import_root` (project file only)
Path to your project root folder (not source folder). If not set, `folders[0].path` will be used.

#### `folders[i].path_source` (project file only)
Path to your source. If not set `folders[i].path` will be used.

Example of settings in project file:
---
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

No imports found for...
---
Or if you see such message in status bar and console:
```
There is no project file, ... will not work without project.
```
You must create project from your working files and folders, you can do it in top menu:  
`Project -> Save project as...`  
Save project file in any place you want.  
Then restart Sublime.  

CHANGELOG
---
| Version | Date        | Description                                             |
|:--------|:------------|:--------------------------------------------------------|
| 1.6.4   | 03 Nov 2017 | Updated `esm-exports` to v0.8.5                         |
| 1.6.3   | 20 Oct 2017 | Fixed #42 settings does not work                        |
| 1.6.2   | 18 Oct 2017 | Fix for empty projects                                  |
| 1.6.0   | 06 Oct 2017 | New feature remove unused imports                       |
| 1.5.0   | 24 Jun 2017 | Added update source modules command                     |
| 1.4.1   | 03 May 2017 | Import tsx/jsx without extension                        |
| 1.4.0   | 29 Mar 2017 | Settings per project                                    |
| 1.3.0   | 23 Mar 2017 | Prevent fail while parse link to not existing directory |
| 1.1.1   | 09 Mar 2017 | Respect exclude_patterns project settings               |
| 1.1.0   | 25 Feb 2017 | Auto update imports when new file saved                 |
|         |             | Unit tests, bug fixing                                  |
|         |             | Parse inner modules                                     |
| 1.0.10  | 30 Jan 2017 | Fixed errors when broken package.json                   |
| 1.0.8   | 24 Jan 2017 | Added .no-sublime-package                               |
| 1.0.7   | 21 Jan 2017 | Fixed #10 incorrect adding to `import as`               |
| 1.0.6   | 10 Jan 2017 | Updated esm-exports modules to 0.3.2                    |
| 1.0.5   | 10 Jan 2017 | Updated esm-exports modules to 0.3.1                    |
| 1.0.3   | 26 Dec 2016 | Setting `space_around_braces`                           |
| 1.0.1   | 19 Dec 2016 | Fixed loading settings bug                              |
| 1.0.0   | 18 Dec 2016 | First release                                           |

TODO
---
* parse single file
* Handle all selections
* watch for project file changes
* update imports on adding file