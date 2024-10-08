# fisheye
A bigger version of my `shrimp` package, now supporting multi-file handling in just one Database object!!!!!!!
A database is now a directory storing "chunks" aka seperate JSON files.

Easy and intuitive to setup, run and debug with internal logging systems

# Examples
## Setup a database directory
```py
import fisheye

db = fisheye.Database()
db._bind('database')
db.makechunks('default')
default = db.accesschunk('default')

db._unbind()
```
