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

## Quick setup method
```py
import fisheye

db = fisheye.Database()
db.quicksetup('database') # Does everything you need to do in just one line
db._unbind()
```

## Chunk operations
```py
import fisheye

db = fisheye.Database()
db._bind('database')
db.makechunks('default')
default = db.accesschunk('default')

db.delchunks(default) # Delete the chunk for example

table = fisheye.Table({'test':'data'})
table.addrecord('something', {'something data':'something something data'})
db.makechunks('default') # re making the 'default' chunk
default = db.accesschunk('default')
default.write(table) # Override current data with 'table'

db.writechunks(default)

db._unbind()
```
