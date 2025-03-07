# dbc.py holds functions that give a db connection
# supported: mssql and sqlite

# functions:
# dbconnect
# dbinfo
# dburi
# _connection_string

# db interface imports are optional, so that the user can pip install only those he needs.

try:
    import pyodbc
except:
    pyodbc = None
import configparser
import os
from pathlib import Path
try:
    import sqlite3
except:
    sqlite = None

# connection returns a database connection
def dbconnect(target=None):
    if target == None:
        target = 'num_test'
    info = dbinfo(target)
    # connect differently depending on database type
    if info['type'] == "sqlite":
        return sqlite3.connect(info['database'])
    else:
        return pyodbc.connect(_connection_string(target))

# connection_string returns a connection string
def _connection_string(target='num_test') -> str:
    info = dbinfo(target)

    connection_string = 'DRIVER=' + info['driver'] + ';SERVER=' + info['server'] + ';PORT=' + info['port'] + ';DATABASE='+ info['database'] + ';UID=' + info['username'] + ';PWD=' + info['password'] + '; encrypt=no;'

    return connection_string

# dburi returns a database uri
def dburi(target = 'num_test'):
    info = dbinfo(target)
    
    # for uri see https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    # ?driver= from https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
    uri = "mssql+pyodbc://" + info['username'] + ":" + info['password'] + "@" + info['server'] + ":" + info['port'] + "/" + info['database'] + "?driver=" + info['driver'] + "&encrypt=no"
    return uri

# dbinfo gets database info from .ini files
def dbinfo(target):
    # we don't want the db.ini in the same directory as the code, so that it does't accidentaly end up in github. set db.ini's location in dbc.ini, along with the db driver the client uses
    ini = configparser.ConfigParser()
    base_name = os.path.dirname(__file__)
    ini.read(os.path.join(base_name, 'dbc.ini'))
    dbinipath = ini["db"]["ini"]

    # read db auth info from db.ini
    config = configparser.ConfigParser()
    config.read(Path(dbinipath))
    #print(dict(config))
    dbtype = config[target]['type']
    info = {
        'type': dbtype,
        'database': config[target]["database"],
        'username': config[target]["username"] if "username" in config[target] else None,
        'password': config[target]["password"] if "password" in config[target] else None,
        'server': config[target]["server"] if "server" in config[target] else None,
        'port': config[target]["port"] if "port" in config[target] else None,
        # read the driver from dbc.ini
        'driver': ini["driver"][dbtype] if ("driver" in ini and dbtype in ini["driver"]) else None
    }
    # driver = '{SQL Server}' # for num-etl
    # driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1' # for ubuntu on wsl
    return info
