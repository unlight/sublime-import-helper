### [4.1.1](https://github.com/unlight/sublime-import-helper/compare/v4.1.0...v4.1.1) (2022-05-04)


### Bug Fixes

* Improve detect node executable ([a10dcca](https://github.com/unlight/sublime-import-helper/commit/a10dccab287abff938323d7152c9fd2adb419561)), closes [#107](https://github.com/unlight/sublime-import-helper/issues/107)

## [4.1.0](https://github.com/unlight/sublime-import-helper/compare/v4.0.0...v4.1.0) (2021-09-16)


### Features

* Setting for space in braces `insert_space_in_braces` ([df0d246](https://github.com/unlight/sublime-import-helper/commit/df0d246625eae590081e8823bde9666dfd500933))


### Bug Fixes

* Exception must inherit BaseException ([7ceb54f](https://github.com/unlight/sublime-import-helper/commit/7ceb54f0798298baf274631c9889f3e48043930d))

## [4.0.0](https://github.com/unlight/sublime-import-helper/compare/v3.1.0...v4.0.0) (2021-09-11)


### ⚠ BREAKING CHANGES

* Require Node.js 12.0+

### Features

* Setting to disable semicolon ([4319e8d](https://github.com/unlight/sublime-import-helper/commit/4319e8df9644829b7b6dd6f4ce3e6edabc38fcb2))


### Miscellaneous Chores

* Updated packages ([78b8fa1](https://github.com/unlight/sublime-import-helper/commit/78b8fa18e527e89c202f4f5b7d9244a9b858cbd8))

# [3.1.0](https://github.com/unlight/sublime-import-helper/compare/v3.0.2...v3.1.0) (2020-06-30)


### Bug Fixes

* Some imports from ambient modules are missing ([098fe1b](https://github.com/unlight/sublime-import-helper/commit/098fe1bf90a3049dbcc1b45d2788506b22746ef4))


### Features

* Sorted named imports ([12e2370](https://github.com/unlight/sublime-import-helper/commit/12e237049ec30a9f4c951bc5bf02a57d7eff0144)), closes [#48](https://github.com/unlight/sublime-import-helper/issues/48)

## [3.0.2](https://github.com/unlight/sublime-import-helper/compare/v3.0.1...v3.0.2) (2020-06-12)


### Bug Fixes

* Export node modules from non-current directory does not work ([bbbd4c4](https://github.com/unlight/sublime-import-helper/commit/bbbd4c429294ec8d5b515d294e6fbec19d182161))

## [3.0.1](https://github.com/unlight/sublime-import-helper/compare/v3.0.0...v3.0.1) (2020-06-10)


### Bug Fixes

* Added no-warnings argument https://nodejs.org/api/cli.html#cli_no_warnings ([b6d78eb](https://github.com/unlight/sublime-import-helper/commit/b6d78ebc9a405e6afdd5a744c90bf2c824597912)), closes [#80](https://github.com/unlight/sublime-import-helper/issues/80)

# [3.0.0](https://github.com/unlight/sublime-import-helper/compare/v2.3.2...v3.0.0) (2020-06-09)


### Bug Fixes

* Added scope TypeScript unit test ([2760b6c](https://github.com/unlight/sublime-import-helper/commit/2760b6ca883e17b4228def45a26cfd1c98d94021))
* Panel items functions did not get call ([2846934](https://github.com/unlight/sublime-import-helper/commit/284693467d202a1d18e925e01b33a31fced22008))


### Features

* Auto detect import root from several source folders ([ed4a646](https://github.com/unlight/sublime-import-helper/commit/ed4a646a512b5f952c899178451278e9a49eba6f))
* New bundler (webpack) ([e1dd06a](https://github.com/unlight/sublime-import-helper/commit/e1dd06aa259c3ab9b4348f9146ec253b90b1afad))
* Removed `from_semicolon` setting ([48393dc](https://github.com/unlight/sublime-import-helper/commit/48393dc4123009560356d3a7769dcf0a2c246df6))
* Removed `space_around_braces` setting ([12c7732](https://github.com/unlight/sublime-import-helper/commit/12c7732f426232031042e097b975137b7a1ff7e5))
* Removed unused files and settings ([8f78077](https://github.com/unlight/sublime-import-helper/commit/8f78077758f3318a5a0bb25d2a353ab5692fc775))
* Removed unused imports command ([b11a5de](https://github.com/unlight/sublime-import-helper/commit/b11a5de3797b251a76b2891b5d22e6164cfe6d14))
* Replaced esm-exports by import-adjutor ([bea6160](https://github.com/unlight/sublime-import-helper/commit/bea61609690c0d5047e33313629bc5f2aa5a6f31))
* Setting `import_path_mapping` changed to `enabled` by default ([03ff2c3](https://github.com/unlight/sublime-import-helper/commit/03ff2c3c6d1f04ac2de11f447f43ce6ab918b1e2))
* Setting `insert_position` removed ([01eac3f](https://github.com/unlight/sublime-import-helper/commit/01eac3f6df909986afba1e93e4c4c58de2055686))


### Performance Improvements

* Load node_modules one by one from source folders ([fd8dbf1](https://github.com/unlight/sublime-import-helper/commit/fd8dbf13332a9742cc412b3d115796d59dcb0189))
* Moved cut path outside of loop ([65605c2](https://github.com/unlight/sublime-import-helper/commit/65605c2dee81b50360b4c27a72da2d1126b2c804))


### BREAKING CHANGES

* Auto detect import root from several source folders (project file is not required)
* Removed unused `import_no_match_count` setting
* Setting `import_path_mapping` changed to `enabled` by default
* Removed `space_around_braces` setting, now it is always true
* Removed `from_semicolon` setting, now it is always true
* Removed unused imports command, the replacement is eslint/tslint rules with fixers https://github.com/cartant/tslint-etc (no-unused-declaration)
* New bundler (webpack)
* Replaced esm-exports by import-adjutor, required Node.js 10+

### Old Changelog

| Version | Date        | Description                                                                                                     |
|:--------|:------------|:----------------------------------------------------------------------------------------------------------------|
| 2.3.2   | 27 May 2020 | Improved import to import default statement                                                                     |
| 2.3.1   | 03 Nov 2019 | Fixed [#71](https://github.com/unlight/sublime-import-helper/issues/71)                                         |
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
