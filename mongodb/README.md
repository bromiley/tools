# MongoDB 2.x Log Parsing Scripts

## mongo_session_stats.py
Utilize this script to analyze what happened during a MongoDB connected session. Activity is based on connection ID, which may be duplicated across multiple log files.

### Versioning
2016-01-29 - v0.1
  
  * Initial script release

### Dependencies
  
  * Python 2.7+ (not tested on Python3; probably won't work)

### Future Plans
  - [ ] Expanded search options (commands, getmore, etc.)
  - [ ] Expanded output options
  - [ ] Include bytes and documents returned
  - [ ] Parsing of folder of MongoDB log files
  - [ ] Parsing of a compressed file of MongoDB logs
  - [ ] Potentially integrate with timeframe script (discern with flags?)

-----

## mongo_timeframes.py
Utilize this script to create timeframes from a single MongoDB log file. Timeframes are based on connection IDs, which may be duplicated through multiple log files.

### Versioning
2016-01-28 - v0.1
  
  * Initial script release

### Dependencies
  
  * Python 2.7+ (not tested on Python3; probably won't work)

### Future Plans
  - [ ] Expanded output options
  - [ ] Include length of sessions
  - [ ] Better timezone handling
  - [ ] Parsing of folder of MongoDB log files
  - [ ] Parsing of a compressed file of MongoDB logs
