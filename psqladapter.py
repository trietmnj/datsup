"""
The contained DatabaseManager class aims to maintain a single interface to a 
PostgreSQL database during a running session
"""
import psycopg2 as pg2
from pandas import DataFrame
import pandas as pd


class DatabaseManager:
    """
    Manages the connection to a PostgreSQL database.
    Make sure to run .commit() to update changes.

    :methods:
        __init__
        __del__
        createTable
        commit
        getData
        testQuery
        close

    :attributes (read-only):
        conn
        cursor
    """
    @property
    def conn(self):
        '''Ensures self._conn will not be modified after init'''
        return self._conn

    @property
    def cursor(self):
        '''Ensures self._cursor will not be modified after init'''
        return self._cursor

    def commit(self):
        '''Commit pending transactions to database'''
        self.conn.commit()

    def __init__(self, host, database, user, password):
        '''Setup connection'''
        self._conn = pg2.connect(host=host, database=database, user=user, password=password)
        self._cursor = self._conn.cursor()

    def __del__(self):
        '''Close connection to database'''
        self.close()

    def createTable(self, table: str, dataVars: dict, foreignKeys=[], drop=False, verify=False):
        '''
        Drop and recreate table. Must set verify to authenticate action.

        db.createTable(
            table='customer', 
            dataVars=dict(name='VARCHAR(20)', address='VARCHAR(50)'),
            foreignKeys=['store', 'address']
            drop=True,
            verify=True
            )
        '''

        if not verify:
            raise Exception('Must set verify=True to create new table')
        if drop:
            sql = 'DROP TABLE IF EXISTS {};'.format(table)
            self.cursor.execute(sql)
            self.commit()

        # create table
        sql = '''CREATE TABLE IF NOT EXISTS {} (
            {}_id SERIAL PRIMARY KEY'''.format(table, table)
        for key in foreignKeys:
            sql += ', {}_id INTEGER'.format(key)
        for var in dataVars.items():
            sql += ', {} {}'.format(var[0], var[1])
        sql += ');'
        self.cursor.execute(sql)
        self.commit()

    def getData(self, sql: str) -> DataFrame:
        '''
        Returns query data inside a DataFrame
        
        data = db.get_datacur.execute(
            ('SELECT * FROM customer')
        '''
        if 'drop' in sql:
            raise Exception('SQL is specifying a drop command')
        return(pd.read_sql(sql, self._conn))

    def testQuery(self, sql):
        '''Limit selected data to the first 10 entries'''
        sql += " limit 10"
        return self.getData(sql)

    def close(self):
        """
        Close cursor and conn
        """
        self.cursor.close()
        self.conn.close()

    def runSQL(self, sql: str, verify=False):
        "Run manual SQL, must verify"
        if not verify:
            raise Exception('Must set verify=True to run custom SQL')

        self.cursor.execute(sql)
        self.commit()
