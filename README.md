sublime-import-helper
=====================
A Sublime Text Plugin that helps you to import your modules.

Supported Languages
---
* TypeScript

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

Project Settings
---
#### `sourceRoot`
Path to source folder. If not set, directory of `folders[0].path` will be used.

TODO
---
* insert to the end of imports block
* Use status_message for errors (node not found, etc.)
* support js
* TODO in *.py files
* watch for project file changes
* update imports on adding file