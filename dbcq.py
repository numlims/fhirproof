# dbcq.py holds functions for db connection and querying

# functions:
# query: query without fetch
# qfa: query fetch all
# qfad: query fetch all dict
# info: db info

from dbc import *
# import jsonpickle
import argparse
import pyodbc
import sys

class dbcq:

    # init remembers the target, a config chapter name of db.ini
    def __init__(self, target):
        self.target = target
        self.info = dbinfo(target)

    # query executes query with optional values
    def query(self, query, *values):
        conn = dbconnect(target=self.target)
        cursor = conn.cursor()
        cursor.execute(query, *values)
        conn.commit()
        conn.close()

    # qfa executes query with optional values and returns results
    def qfa(self, query, *values):
        conn = dbconnect(target=self.target)
        cursor = conn.cursor()
        cursor.execute(query, *values)
        rows = cursor.fetchall()
        conn.commit()
        conn.close()

        return rows

    # qfad returns query result as array of dicts, e.g. for json parsing
    def qfad(self, query, *values):
        # for mssql, fold in cursor description of row
        if self.info["type"] == "mssql":
            rows = self.qfa(query, *values)
            dicts = [self._row_to_dict(row) for row in rows]
            return dicts
        elif self.info["type"] == "sqlite":
            # for sqlite, use row factory
            # from https://stackoverflow.com/a/41920171
            conn = dbconnect(target=self.target)
            cursor = conn.cursor()
            cursor.row_factory = sqlite3.Row
            cursor.execute(query, values) # pass as tuple, see https://stackoverflow.com/a/16856730
            rows = cursor.fetchall()
            conn.commit()
            conn.close()

            dicts = [dict(row) for row in rows]
            return dicts

    # info returns database info
    def info(self):
        return self.info
    
    # _row_to_dict turns pyodbc-rows to dict
    def _row_to_dict(self, row):
        # lowercase column names
        columns = [tup[0].lower() for tup in row.cursor_description]
        # use column names as dict keys
        return dict(zip([c for c in columns], row))


# main
if __name__ == "__main__":
    # get database
    target = sys.argv[1]

    # start dbcq
    db = dbcq(target)

    # get query
    query = sys.argv[2]

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="a database target in db.ini")
    parser.add_argument("query", nargs="?", help="a sql query")
    parser.add_argument("-f", help="a sql query file", required=False)
    args = parser.parse_args()

    # if file given, take query from file
    if args.f is not None:
        query = open(args.f, "r").read()
    else: # else take query from commandline
        query = parser.query

    print(f"file: {args.f}")

    print(f"query: {query}")

    # query and print result
    #print(jsonpickle.encode(db.qfad(query)))
    # jsonpickle puts decimals in wrappers.
    # could our db output give simpler types?
    # for now like this

    print(db.qfad(query))
