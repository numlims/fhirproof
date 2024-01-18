# dbcon.py holds functions that give a db connection

import pyodbc
import configparser
import os

# getDatabaseConnection returns the database connection
def get_database_connection(target_system: str = 'num_prod', database=None):
    return pyodbc.connect(get_conn_str(target_system, database))

#getConnStr returns the connection string
def get_conn_str(target_system: str = 'num_prod', database=None) -> str:
    config = configparser.ConfigParser()
    base_name = os.path.dirname(__file__)
    config.read(os.path.join(base_name, 'db.ini'))
    if database is None:
        database = config[target_system]['database_name']
    # database = "KAIROS_SPRING"
    username = config[target_system]['username']
    password = config[target_system]['password']
    server = config[target_system]['server']
    # driver = '{SQL Server}' # for num-etl
    driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1' # for ubuntu on wsl
    port = config[target_system]['port']

    CONNECTION_STRING = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password+'; encrypt=no;'

    return CONNECTION_STRING


# query executes query with optional values
def query(query, *values):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(query, *values)
    conn.commit()
    conn.close()

# query_fetch_all executes query with optional values and returns results
def query_fetch_all(query, *values):
    conn = get_database_connection()
    cursor = conn.cursor()
    cursor.execute(query, *values)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()

    return rows

# qfad (query fetch all dict) returns query result as array of dicts, e.g. for json parsing
def qfad(query, *values):
    rows = query_fetch_all(query, *values) # values is a tuple, expand tuple with *
    dicts = [row_to_dict(row) for row in rows]
    return dicts

# row_to_dict turns row to dict
def row_to_dict(row):
    return dict(zip([t[0] for t in row.cursor_description], row))
