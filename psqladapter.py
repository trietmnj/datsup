"""
The contained DatabaseManager class aims to maintain a single interface to a PostgreSQL
    database during the session
"""
import configparser
import psycopg2 as pg2
from pandas import DataFrame
import pandas as pd
from typing import List

class DatabaseManager:
    """
    Manages the connection to a PostgreSQL database. Make sure to run .commit() to update changes.

    :methods:
        __init__:
        create_table: 

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

    def create_table(self, table:str, data_vars: dict, foreign_keys=[], drop=False, verify=False):
        '''
        Drop and recreate table. Must set verify to authenticate action.
        
        db.create_table(
            table='customer', 
            data_vars=dict(name='VARCHAR(20)', address='VARCHAR(50)'),
            foreign_keys=['store', 'address']
            drop=True,
            verify=True
            )
        '''

        if not verify:
            raise Exception('Must set verify=True to create new table')
        if drop:
            sql = 'DROP TABLE IF EXISTS {};'.format(table)
            self.cursor.execute(sql)

        foreign_keys = [str.lower() for str in foreign_keys]
        # create table
        sql = '''CREATE TABLE IF NOT EXISTS {} (
            {}_id SERIAL PRIMARY KEY'''.format(table, table)
        for key in foreign_keys:
            sql += ', {}_id INTEGER'.format(key)
        for var in data_vars.items():
            sql += ', {} {}'.format(var[0], var[1])
        sql += ');'
        self.cursor.execute(sql)

    #########################################################
    #   From prior project with sqlite - reimplement!!!
    #########################################################

    # def insert_row(self, table:str, data): 
    #     """
    #     Insert data row wise into a single table. Returns primary key id
    #     """
    #     if not isinstance(data, dict):
    #         raise TypeError('values should be a dict')

    #     vars = ', '.join(list(data.keys()))
    #     questions = ', '.join(['?' for _ in data])
    #     values = tuple(data.values())

    #     sql = 'INSERT OR IGNORE INTO {} ({}) VALUES ({})'.format(table, vars, questions)
    #     self.cursor.execute(sql, values)

    #     conditions = 'AND '.join([' {}=? '.format(k) for k in data.keys()])
    #     sql = 'SELECT id FROM {} WHERE {}'.format(table, conditions)
    #     self.cursor.execute(sql, values)
    #     id = self.cursor.fetchone()[0]

    #     if id is None:
    #         raise Exception('Unable to retrieve id from {}'.format(table))
    #     return id

    def get_data(self, sql:str) -> DataFrame:
        '''
        Returns query data inside a DataFrame
        
        data = db.get_data('SELECT * FROM customer')
        '''
        if 'drop' in sql:
            raise Exception('SQL is specifying a drop command')
        return(pd.read_sql(sql, self._conn))

    def test_query(self, sql):
        '''Limit selected data to the first 5 entries'''
        sql += " limit 5"
        return self.get_data(sql)

    def close(self):
        """
        Close cursor and conn
        """
        self.cursor.close()
        self.conn.close()

    




