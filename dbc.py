# dbcon.py holds functions that give a db connection

# functions:
# connection
# connection_string
# db_uri

import pyodbc
import configparser
import os

# connection returns a database connection
def connection(target=None):
    if target == None:
        target = 'num_test'
    return pyodbc.connect(connection_string(target))

# connection_string returns a connection string
def connection_string(target='num_test') -> str:
    config = configparser.ConfigParser()
    base_name = os.path.dirname(__file__)
    config.read(os.path.join(base_name, 'db.ini'))
    database = config[target]['database_name']
    username = config[target]['username']
    password = config[target]['password']
    server = config[target]['server']
    # driver = '{SQL Server}' # for num-etl
    driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1' # for ubuntu on wsl
    port = config[target]['port']

    CONNECTION_STRING = 'DRIVER=' + driver + ';SERVER=' + server + ';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+password+'; encrypt=no;'

    return CONNECTION_STRING

# db_uri returns a database uri
def db_uri(target = 'num_test'):
    config = configparser.ConfigParser()
    base_name = os.path.dirname(__file__)
    config.read(os.path.join(base_name, 'db.ini'))
    database = config[target]['database_name']
    username = config[target]['username']
    password = config[target]['password']
    server = config[target]['server']
    # driver: see https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
    # driver = 'SQL Server' # {SQL Server} with curly braces doesn't work for sqlalchemy with pyodbc
    driver = '/opt/microsoft/msodbcsql18/lib64/libmsodbcsql-18.3.so.2.1' # for ubuntu on wsl
    port = config[target]['port']

    # for uri see https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    # ?driver= from https://medium.com/@anushkamehra16/connecting-to-sql-database-using-sqlalchemy-in-python-2be2cf883f85
    uri = "mssql+pyodbc://" + username + ":" + password + "@" + server + ":" + port + "/" + database + "?driver=" + driver + "&encrypt=no"
    # uri = "mssql+{SQL Server}://" + username + ":" + password + "@" + server + ":" + port + "/" + database
    # uri = "mssql+" + driver + "://" + username + ":" + password + "@" + server + ":" + port + "/" + database
    return uri