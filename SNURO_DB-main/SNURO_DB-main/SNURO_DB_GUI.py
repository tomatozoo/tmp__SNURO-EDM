# -*- coding: utf-8 -*-
"""
@author: LKM
"""
from PyQt5 import uic, QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore    import *
from SNURO_DB import SNURO_DB
import configparser, socket, time, os, pickle
import numpy as np

filename = os.path.abspath(__file__)
dirname = os.path.dirname(filename)

uifile = dirname + '/%s.ui' % os.path.basename(filename[:-7])
Ui_Form, _ = uic.loadUiType(uifile)

class SNURO_DB_GUI(QtWidgets.QMainWindow, Ui_Form):
     
    def closeEvent(self, e):
        self._db.disconnect()
            
    def __init__(self, instance_name='SNURO_DB', parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)
        
        self._db = SNURO_DB()
        self.connect_ui()
        # self.thread = Thread()    
        
    
    def connect_ui(self):
        self.BTN_LOGIN.clicked.connect(self._log_in)
        self.BTN_FETCH.clicked.connect(self._fetch_table)
        self.LST_DB.itemDoubleClicked.connect(self._fetch_table)
        self.LST_TABLE.itemDoubleClicked.connect(self._fetch_data)
    
    def _log_in(self):
        self._DNS = self.TXT_DNS.text()
        self._PORT = int(self.TXT_PORT.text())
        self._ID = self.TXT_ID.text()
        self._PW = self.TXT_PW.text()
        self._db.RescanID(DB_IP = self._DNS, DB_PORT = self._PORT,
                          DB_NAME='mysql', user_id = self._ID, password=self._PW)
        try:
            self._db.connect()
            self._Login_success()
        except:
            self._Login_failed()

    def _Login_success(self):
        self.LBL_LOGIN.setText('Logged In')
        self.LBL_LOGIN.setStyleSheet('background-color:rgb(222, 222, 222); color: rgb(0, 255, 0);')
        self._update_db_list()
        
    def _Login_failed(self):
        self.LBL_LOGIN.setText('Log In Failed')
        self.LBL_LOGIN.setStyleSheet('background-color:rgb(222, 222, 222); color: rgb(255, 0, 0);')
    
    def _update_db_list(self):
        self._db.ScanDB()
        for i, db in enumerate(self._db._DB_list):
            self.LST_DB.insertItem(i, db)    
    
    def _fetch_table(self):
        self._selected_db = self.LST_DB.selectedItems()[0].text()
        if not self._selected_db == None:
            self._db.UseDB(self._selected_db)
            self._db.ScanTable()
            for i, table in enumerate(self._db._Table_list):
                self.LST_TABLE.insertItem(i, table)
        else:
            print('No DB selected')
        
    def _fetch_data(self):
        self._selected_table = self.LST_TABLE.selectedItems()[0].text()
        if not self._selected_table == None:
            self._db.UseTable(self._selected_table)
            self._table_data = self._db.GetTableData()
            self._table_desc = self._db.GetTableDescription()
            self._Update_Table_Contents()
        else:
            print('No TABLE selected')
    
    def _Update_Table_Contents(self):
        columns = self._table_desc['Field']
        num_rows = len(self._table_data)
        self.TBL_CONTENTS.setColumnCount(len(columns))
        self.TBL_CONTENTS.setRowCount(num_rows)
        
        self.TBL_CONTENTS.setHorizontalHeaderLabels(columns)
        for i in range(len(columns)):
            self.TBL_CONTENTS.horizontalHeaderItem(i).setTextAlignment(Qt.AlignCenter)

        for row, data in enumerate(self._table_data):
            for column, key in enumerate(columns):
                item = data[key]
                self.TBL_CONTENTS.setItem(row, column, QTableWidgetItem(str(item)))
        
# class Thread(QThread):
        
#     def __init__(self):
#         super().__init__()
#         self.run_flag = False
        
#     def run(self):
#         while self.run_flag:
#             pass
            
        
#%%
if __name__ == "__main__":
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication([])
    # app.setStyleSheet(RIGOL_CSS) 
    db = SNURO_DB_GUI(instance_name='SynthHD')
    
    # db.show()
