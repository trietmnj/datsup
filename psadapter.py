import configparser
import sqlite3

import sqlalchemy

from modules import exceptions


class DatabaseManager:
    """
    Feed in dataframe to save into database

    :methods:
        _init__:
        _load_settings: 
        _setup_connection: 
        _create_table: 

    :attributes (read-only):
        conn
        cursor
        config

    """

    @property
    def conn(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    @property
    def config(self):
        return self._config

    def commit(self):
        self.conn.commit()

    def _create_table(self, table, data_vars, foreign_keys=[], drop=False):
        '''
        Create a table (primary key is automatically created)
        :param table:
        :param data_vars: dict containing column name and settings
            data_vars = {'col1': 'REAL NOT NULL', 'col2': 'TEXT UNIQUE'}
        :param foreign_keys: list table names corresponding to end of foreign key
            foreign_keys = ['security', 'exchange']
        :param drop: invoke 'DROP TABLE IF EXISTS' if True
        '''

        foreign_keys = [str.lower() for str in foreign_keys]

        if drop:
            sql = 'DROP TABLE IF EXISTS {};'.format(table)
            self._cursor.executescript(sql)

        sql = '''CREATE TABLE IF NOT EXISTS {} (
            id INTEGER NOT NULL PRIMARY KEY UNIQUE'''.format(table)

        for key in foreign_keys:
            sql += ', {}_id INTEGER'.format(key)

        for var in data_vars.items():
            sql += ', {} {}'.format(var[0], var[1])

        sql += ');'

        self.cursor.executescript(sql)

    def _insert_row(self, table, data): 
        """
        Insert data row wise into a single table. Returns primary key id
        """
        if not isinstance(data, dict):
            raise TypeError('values should be a dict')

        vars = ', '.join(list(data.keys()))
        questions = ', '.join(['?' for _ in data])
        values = tuple(data.values())

        sql = 'INSERT OR IGNORE INTO {} ({}) VALUES ({})'.format(table, vars, questions)
        self.cursor.execute(sql, values)

        conditions = 'AND '.join([' {}=? '.format(k) for k in data.keys()])
        sql = 'SELECT id FROM {} WHERE {}'.format(table, conditions)
        self.cursor.execute(sql, values)
        id = self.cursor.fetchone()[0]

        if id is None:
            raise exceptions.DbRetrievingError('Unable to retrieve id from {}'.format(table))

        return id

    def _load_settings(self, config_file):
        '''
        Load settings from file
        '''
        self._config = configparser.ConfigParser()
        self._config.read(config_file)

    def _setup_connection(self):
        """
        Setup conn and cursor object
        """

        if not hasattr(self, 'config'):
            raise exceptions.DbRetrievingError('Unable to retrieve config from instance.')

        self._conn = sqlite3.connect(self.config['DEFAULT']['DatabasePath'])
        self._cursor = self.conn.cursor()

    def close(self):
        """
        Close cursor and conn
        """
        self.cursor.close()
        self.conn.close()


    # def _select_columns(self, tab_col, foreign_keys=None): #TODO
    #     """
    #     Select data 
    #     :param tab_col: List containing desired columns for retrieval with format: 
    #         ['Table1.column1', 'Table2.column2', ...]
    #     :
    #     """

    #     field

    #     if len(tab_col) == 1:
            
    #     else:

    #     tables = ' JOIN '.join([column.split('.')[0] for column in tab_col])


    #     columns = ', '.join(columns)
    #     sql = 'SELECT {} FROM {}'.format(columns, tables)

    #     self.cursor.execute(sql,)
    




