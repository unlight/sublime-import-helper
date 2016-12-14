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
2. Press `ctrl+alt+i`, or select `Import Helper: Insert import` from command panel.

#### List imports
1. Press `alt+i, alt+l`, or select `Import Helper: List imports` from command panel.

Project Settings
---
#### `sourceRoot`
Path to source folder. If not set, directory of `folders[0].path` will be used.

TODO
---
* add re-read packages command
