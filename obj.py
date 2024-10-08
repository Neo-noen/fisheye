from .logger import log, BaseLogTypes
import json, os

class Chunk:
    def __init__(chunk, filepath: str):
        """A chunk object used to access a chunk file."""

        chunk.chunkfile = filepath
        chunk.chunkname = os.path.basename(filepath)
        chunk.chunkdata = None

        with open(chunk.chunkfile, 'r') as chunkfile:
            chunk.chunkdata = json.load(chunkfile)

    def write(chunk, table: 'Table'):
        """Write the `table` parameter data to the chunk"""

        if table.data != None:   
            log(BaseLogTypes.INFO, f'Writing table data to chunk "{chunk.chunkname}".')
            chunk.chunkdata = table.data.copy()
        else:
            log(BaseLogTypes.ERROR, 'Table data is null')

    def insert(chunk, table: 'Table'):
        """Insert a table data into the chunk"""

        if table.data != None:
            log(BaseLogTypes.INFO, f'Inserting table data into chunk "{chunk.chunkname}".')
            for chunkkey in table.data.keys():
                chunk.chunkdata[chunkkey] = table.data[chunkkey]
        else:
            log(BaseLogTypes.ERROR, 'Table data is null')

class Table:
    def __init__(table, data: dict):
        """A table object"""

        table.data = data

    def addrecord(table, recordname: str, recorddata: dict) -> None:
        if recordname in table.data.keys():
            log(BaseLogTypes.WARN, f'"{recordname}" record is already in the table')
        else:
            table.data[recordname] = recorddata
            log(BaseLogTypes.INFO, f'Created record "{recordname}"')

    def delrecord(table, recordname: str) -> None:
        if recordname not in table.data.keys():
            log(BaseLogTypes.ERROR, f'"{recordname}" record was not found')
        else:
            del table.data[recordname]
            log(BaseLogTypes.INFO, f'Deleted record "{recordname}"')    
    
    def editrecord(table, recordname: str, newdata: dict) -> None:
        if recordname not in table.data.keys():
            log(BaseLogTypes.ERROR, f'"{recordname}" record was not found')
        else:
            table.data[recordname] = newdata
            log(BaseLogTypes.INFO, f'"{recordname}" completed edit')

    def drop(table) -> None:
        """Reset the table or delete it"""

        log(BaseLogTypes.WARN, f'Dropping table')
        table.data = None