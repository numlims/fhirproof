# dbcq.py holds functions for db connection and querying

# functions:
# qfa: query fetch all
# qfad: query fetch all dict
# row_to_dict

from dbc import *
import pyodbc

class dbcq:

	# init remembers the target, a config chapter name of db.ini
	def __init__(self, target):
		self.target = target

	# query executes query with optional values
	def query(self, query, *values):
	    conn = connection(target=self.target)
	    cursor = conn.cursor()
	    cursor.execute(query, *values)
	    conn.commit()
	    conn.close()

	# qfa executes query with optional values and returns results
	def qfa(self, query, *values):
	    conn = connection(target=self.target)
	    cursor = conn.cursor()
	    cursor.execute(query, *values)
	    rows = cursor.fetchall()
	    conn.commit()
	    conn.close()

	    return rows

	# qfad returns query result as array of dicts, e.g. for json parsing
	def qfad(self, query, *values):
	    rows = self.qfa(query, *values)
	    dicts = [self.row_to_dict(row) for row in rows]
	    return dicts

	# row_to_dict turns row to dict
	def row_to_dict(self, row):
	    # lowercase column names
	    columns = [tup[0].lower() for tup in row.cursor_description]
	    # use column names as dict keys
	    return dict(zip([c for c in columns], row))

