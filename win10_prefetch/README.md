# Windows 10 Prefetch Parser

This is a simple script that can be utilized to parse Windows 10 Prefetch files. Note that it requires 'libscca' to be installed. I tested this on Linux systems, both a custom-build and the SIFT Workstation, release by SANS.

### Versioning
2016-02-03 - v0.3

  * JSON Output option
  * Volume Information Included
  * Output file option
  * Cleaned up code a bit; still have optimizations left :(

2016-01-18 - v0.2

  * Code optimizations

2016-01-18 - v0.1
  
  * Initial script release

### Dependencies
  
  * Python 2.7+ (not tested on Python3; probably won't work)
  * libscca, which can be downloaded [here](https://github.com/libyal/libscca). Thanks to Joachim Metz for the helpful library.

### Future Plans
  - [X] Expanded output options
  - [X] Output volume information if user wants it
  - [ ] Better error handling and checksums. For example, output all PF files that were not parsed during a directory parse
  - [ ] Figure out how to handle file and file metrics output
