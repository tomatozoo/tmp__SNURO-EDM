# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 22:47:01 2021

@author: User
"""
import pymysql
import yfinance as yf
import datetime

def requires_connection(func):
    def wrapper(self, *args, **kwargs):
        if hasattr(self, '_conn') and self._conn.open:
            return func(self, *args, **kwargs)
        else:
            raise RuntimeError('{} is called with no connection.'
                               .format(func.__name__))
    return wrapper

class SNURO_DB():
    
    __msg_list = []
    
    def __init__(self, DB_IP=None, DB_PORT=None, DB_NAME='mysql', user_id=None, password=None):
        # Connect to DB
        self.__db_name = DB_NAME
        self.__ip, self.__port = DB_IP, DB_PORT
        self.__id = user_id
        self.__password = password

    def RescanID(self, DB_IP=None, DB_PORT=None, DB_NAME='mysql', user_id=None, password=None):
        # Connect to DB
        self.__db_name = DB_NAME
        self.__ip, self.__port = DB_IP, DB_PORT
        self.__id = user_id
        self.__password = password

    def connect(self):
        self.__conn = pymysql.connect(host=self.__ip, port=self.__port, user=self.__id, password=self.__password,
                       db=self.__db_name, charset="utf8", cursorclass=pymysql.cursors.DictCursor)
        self.__curs = self._conn.cursor()

    @requires_connection
    def disconnect(self):        
        self.__conn.commit()
        self.__conn.close() 

    @requires_connection
    def _SendQuery(self, msg, is_return=False):
        print(msg)
        self.__curs.execute(msg)
        self.__conn.commit()
        if is_return:
            result = self.__curs.fetchall()
            return result
        
    @requires_connection
    def ScanDB(self):
        msg = 'SHOW DATABASES'
        result = self._SendQuery(msg, is_return=True)
        self._DB_list = [r['Database'] for r in result]
        return self._DB_list 

    @requires_connection
    def CreateDB(self, DB_NAME: str):
        if not hasattr(self, '_DB_list'):
            self.ScanDB()
        if not DB_NAME.lower() in self._DB_list:
            msg = 'CREATE DATABASE %s' % (DB_NAME)
            self._SendQuery(msg)
        else:
            raise RuntimeError('DB {} already Exists'.format(DB_NAME.lower()))
        
    @requires_connection
    def UseDB(self, DB_NAME):
        self._DB = DB_NAME.lower()
        if not hasattr(self, '_DB_list'):
            self.ScanDB()
        if self._DB in self._DB_list:
            msg = 'USE %s' % (self._DB)
            self._SendQuery(msg)
            self._Table = None
        else:
            raise RuntimeError('DB {} is not exists'.format(self._DB))
            
    @requires_connection
    def ScanTable(self):
        if hasattr(self, '_DB'):
            # self.UseDB(self._DB)
            key = 'Tables_in_' + self._DB
            msg = 'SHOW TABLES'
            result = self._SendQuery(msg, is_return = True)
            self._Table_list = [r[key] for r in result]
            return self._Table_list
        else:
            raise RuntimeError('DB is not specified. Use DB first')
    
    def UseTable(self, Table_name:str):
        Table_name = Table_name.lower()
        if hasattr(self, '_Table_list'):
            if Table_name in self._Table_list:
                self._Table = Table_name
            else:
                raise RuntimeError('Table {} is not exists in DB {}'.format(Table_name, self._DB))
            print('Table {} is now used'.format(self._Table))
        else:
            raise RuntimeError('Table list is not specified. Scan Table first')
            
    def GetTableData(self):
        if hasattr(self, '_Table'):
            msg = 'SELECT * FROM %s' % self._Table
            self._Table_contents = self._SendQuery(msg, is_return=True)
            return self._Table_contents
        else:
            raise RuntimeError('Table is not specified. Use Table first')

    def GetTableDescription(self):
        if hasattr(self, '_Table'):
            msg = 'DESC %s' % self._Table
            result = self._SendQuery(msg, is_return=True)
            desc = ['Field', 'Type', 'Null', 'Key', 'Default', 'Extra']
            self._Table_desc = {}
            for d in desc:
                self._Table_desc[d] = [r[d] for r in result]
            return self._Table_desc
        else:
            raise RuntimeError('Table is not specified. Use Table first')

    '''
    data_dict
    key: Data Name (EX: Date, Volume, ...)
    value: Data Type (EX: DATE, float, INT, ...)
    '''
    @requires_connection
    def CreateTable(self, Table_name: str, data_dict: dict):
        Table_name = Table_name.lower()
        if hasattr(self, '_DB'):
            self._Table = Table_name
            msg = 'CREATE TABLE %s (' % Table_name
            for key in data_dict.keys():
                msg += '%s %s, ' % (key, data_dict[key])
            msg = msg[:-2] + ')'
            self._SendQuery(msg)
        else:
            raise RuntimeError('DB is not specified')
            
    '''
    data_dict
    key: Data Name
    value: list with values [val1, val2, ...]
    '''
    def InputData(self, data_dict:dict):
        if hasattr(self, '_DB') and hasattr(self, '_Table'):
            msg = "INSERT INTO %s (" % self._Table
            for key in data_dict.keys():
                msg += '%s, ' % key
                len_data = len(data_dict[key])
            msg = msg[:-2] + ') VALUES ('
            for _ in len(data_dict):
                msg += '{}, '
            msg = msg[:-1] + ')'
            
            for i in range(len_data):
                send_data = []
                for key in data_dict.keys():
                    send_data.append(data_dict[key][i])
                msg = msg.format(*send_data)
                self._SendQuery(msg)
        else:
            raise RuntimeError('DB and Table is not specified')

    def DeleteTable(self, Table_name:str):
        msg = 'DROP TABLE IF EXISTS ' + Table_name
        self._SendQuery(msg)

    def GetUsers(self):
        # Get users
        msg = 'USE ' + self.__db_name
        self._SendQuery(msg)
        msg = 'SELECT user, host from USER'
        self._user_list = self._SendQuery(msg, is_return=True)

    @property
    def _conn(self):
        return self.__conn
    @property
    def _curs(self):
        return self.__curs

if __name__ == '__main__':
    # IP = '192.168.0.25'
    DNS = 'snuro-db.iptime.org'
    PORT= 3306
    db = SNURO_DB(DNS, PORT, DB_NAME='mysql', user_id='lkm', password='lkm')
    
# query = 'DESC %s' % list(result[0].values())[0]
# curs.execute(query)
# result = curs.fetchall()
# for r in result:
#     print(r)