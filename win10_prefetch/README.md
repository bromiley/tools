# Windows 10 Prefetch Parser

This is a simple script that can be utilized to parse Windows 10 Prefetch files. Note that it requires 'libscca' to be installed. I tested this on Linux systems, both a custom-build and the SIFT Workstation, release by SANS. Note that this was quickly thrown together; updates and refining to be done.

### Versioning
2016-01-18 - v0.1
  
  * Initial script release

### Dependencies
  
  * Python 2.7+ (not tested on Python3; probably won't work)
  * libscca, which can be downloaded [here](https://github.com/libyal/libscca). Thanks to Joachim Metz for the helpful library.

### Future Plans
  - [ ] Expanded output options
  - [ ] Output volume information if user wants it
  - [ ] Parsing of ZIP files for compressed PF files
