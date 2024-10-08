import os, datetime, json
from typing import Literal, Generator
from .obj import Chunk
from .logger import log,dumplogs, BaseLogTypes, enablelog, disablelog

class Database:
    def __init__(db, max_chunk_files: int = 1000):
        """Defines a `DatabaseManager`, used to manage a database by using the `_bind()` function"""

        db.max_chunk: int = max_chunk_files
        db.last_bind = None
        db.binded_db: str = None

        db.chunksdir = None
        db.log_file = None

    def logsettings(db, disable: bool = False) -> None:
        """Disables or enables logging."""
        if disable == True:
            disablelog()
        else:
            enablelog()

    def quicksetup(db, filepath: str, *init_chunk: str) -> None:
        """Sets up the `DatabaseManager` for quick use."""
        if os.path.exists(filepath):
            log(BaseLogTypes.ERROR, 'Path already exists.')
        else:
            os.makedirs(filepath)
            log(BaseLogTypes.INFO, 'Path created.')
            db._bind(filepath)

            if len(init_chunk) == 0:
                db.makechunks('default_chunk')
                log(BaseLogTypes.INFO, 'Created default chunk.')
            else:
                for chunk in init_chunk:
                    db.makechunks(chunk)
        
            log(BaseLogTypes.INFO, 'Quick setup completed.')
    def _bind(db, path: str = None) -> str:
        """Binds a `DatabaseManager` to a directory if it exists and returns it."""

        log(BaseLogTypes.INFO, '-----START OF DATABASE OPERATIONS-----')

        if path == None:
            log(BaseLogTypes.ERROR, 'Path not provided.')
            return None

        if os.path.exists(path):

            if os.path.isdir(path):
                db.binded_db = path
                log(BaseLogTypes.INFO, f'Binded database path: "{path}"')

                db.last_bind = str(datetime.datetime.now())
                config_path = os.path.join(db.binded_db, 'mark_config.json')

                if os.path.exists(os.path.join(db.binded_db, 'mark_config.json')):
                    log(BaseLogTypes.INFO, 'Found database configuration file.')
                    with open(config_path) as config:
                        data = json.load(config)
                    with open(config_path, 'w') as config:
                        data['last_bind'] = db.last_bind
                        data['max_chunks'] = db.max_chunk
                        json.dump(data, config, indent=1)
                
                else:
                    log(BaseLogTypes.WARN, 'Directory is not configured, creating configuration')

                    with open(config_path, 'w') as config:
                        json.dump({'max_chunks':db.max_chunk,
                                   'last_bind':db.last_bind}, config, indent=1)
                        
                    log(BaseLogTypes.INFO, 'Configurations marked.')

                if os.path.exists(os.path.join(db.binded_db, 'chunks')):
                    log(BaseLogTypes.INFO, 'Found chunk files directory.')
                    db.chunksdir = os.path.join(db.binded_db, 'chunks')
                else:
                    log(BaseLogTypes.WARN, 'Database chunk files directory was not found.')
                    db.chunksdir = os.makedirs(os.path.join(db.binded_db, 'chunks'))

                if os.path.exists(os.path.join(db.binded_db, 'logs.log')):
                    log(BaseLogTypes.INFO, 'Found log file')
                    db.log_file = os.path.join(db.binded_db, 'logs.log')
                else:
                    log(BaseLogTypes.WARN, 'Log file was not found.')
                    with open(os.path.join(db.binded_db, 'logs.log'), 'w') as file:
                        pass
                    log(BaseLogTypes.INFO, 'Created log file')

                log(BaseLogTypes.INFO, 'Binding sucessful.')
                db.chunksdir = os.path.join(db.binded_db, 'chunks')
                return path
            
            elif os.path.isfile(path):
                log(BaseLogTypes.ERROR, 'Provided path was a file path.')
                return None
        else:
            log(BaseLogTypes.ERROR, 'Directory not found.')
            return None
        
    def _unbind(db) -> None:
        """Unbinds the database path from the `DatabaseManager`."""
        if db.binded_db != None:
            db.binded_db = None
            db.chunksdir = None
            log(BaseLogTypes.INFO, 'Unbinded database')
            log(BaseLogTypes.INFO, '-----END OF DATABASE OPERATIONS-----')

            dumplogs(db.log_file)
        else:
            log(BaseLogTypes.WARN, 'No binded database path.')

    def makechunks(db, *chunks: str) -> Chunk:
        """Create `chunks` amount of chunk files directly"""

        if len(chunks) == 0:
            log(BaseLogTypes.ERROR, 'No chunk names provided')
        else:
            for chunk in chunks:
                chunkpath = os.path.join(db.chunksdir, f'{chunk}.json')
                if os.path.exists(chunkpath):
                    log(BaseLogTypes.WARN, f'"{chunk}" chunk already exists.')
                else:
                    with open(chunkpath, 'w') as chunkfile:
                        json.dump({}, chunkfile)
                    log(BaseLogTypes.INFO, f'Made chunk "{chunk}"')
                chunkobj = Chunk(chunkpath)
    
    def delchunks(db, *chunks: str) -> None:
        """Delete `chunks` amount of chunk files directly"""

        if len(chunks) == 0:
            log(BaseLogTypes.ERROR, 'No chunk names provided')
        else:
            for chunk in chunks:
                chunkpath = os.path.join(db.chunksdir, f'{chunk}.json')
                if os.path.exists(chunkpath):
                    log(BaseLogTypes.INFO, f'Deleting "{chunk}" chunk file.')
                    os.remove(chunkpath)
                else:
                    log(BaseLogTypes.ERROR, f'"{chunk}" chunk file not found.')

    def accesschunk(db, chunkname: str) -> Chunk:
        """Gives you a `Chunk` object equivalent of a chunk JSON file"""
        
        chunkpath = os.path.join(db.chunksdir, f'{chunkname}.json')

        if os.path.exists(chunkpath):
            log(BaseLogTypes.INFO, f'Accessing chunk "{chunkname}"')
            return Chunk(chunkpath)
        else:
            log(BaseLogTypes.ERROR, f'"{chunkname}" chunk was not found.')

    def writechunks(db, *chunks: Chunk) -> None:
        """Writes chunk objects to it's JSON file equivalent"""

        for chunk in chunks:
            log(BaseLogTypes.INFO, f'Writing "{chunk.chunkname}" data to file.')
            with open(chunk.chunkfile, 'w') as chunkfile:
                json.dump(chunk.chunkdata, chunkfile, indent=1)
            log(BaseLogTypes.INFO, 'Write operation completed.')

    def _search(db, query: str, type: Literal['table','record'] = 'table') -> tuple:
        """Searches for `query` in the database. `type` can be 'table' or 'record'."""

        results = []

        log(BaseLogTypes.INFO, f'Searching database for "{query}"')

        if type == 'table':
            for chunk in os.listdir(db.chunksdir):
                chunkobj = Chunk(os.path.join(db.chunksdir, chunk))
                if query in chunkobj.chunkdata.keys():
                    results.append({'chunk':chunkobj.chunkname,'table':query,'data':chunkobj.chunkdata[query]})
                
        elif type == 'record':
            for chunk in os.listdir(db.chunksdir):
                chunkobj = Chunk(os.path.join(db.chunksdir, chunk))
                for table in chunkobj.chunkdata.keys():
                    for record in chunkobj.chunkdata[table]:
                        if query == record:
                            recorddata = chunkobj.chunkdata[table][record]
                            results.append({'chunk':chunkobj.chunkname,'table':table, 'data':recorddata})
        
        log(BaseLogTypes.INFO, 'Search completed')
        if len(results) == 0:
            log(BaseLogTypes.INFO, 'No results found')

        return tuple(results)
    
    def _filtersearch(db, search: tuple, filtertype: Literal['chunk', 'table', 'record'], searchfilter: str) -> tuple:
        """Filters search results by chunk name"""

        filtered = []

        log(BaseLogTypes.INFO, f'Filtering by "{filtertype}" with filter query "{searchfilter}"')

        if len(search) == 0:
            log(BaseLogTypes.ERROR, 'No search results provided')
        else:
            for result in search:
                if filtertype == 'chunk':
                    if result['chunk'] == searchfilter:
                        filtered.append(result)
                elif filtertype == 'table':
                    if result['table'] == searchfilter:
                        filtered.append({'table':result['table'], 'data':result['data']})
                elif filtertype == 'record':
                    for record in result['data'].keys():
                        if record == searchfilter:
                            filtered.append({'table':result['table'], record:result['data'][record]})

        return tuple(filtered)