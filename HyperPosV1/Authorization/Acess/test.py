import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_test(QtWidgets.QDialog):

    def __init__(self):
        super(CL_test, self).__init__()
    def load(self):
        loadUi('../Presentation/test.ui', self)
        # index = self.formLayout.count()
        # print(index)
        # while (index >= 0):
        #     myWidget =  self.formLayout.itemAt(index).widget()
        #     myWidget.setEnabled(False)
        #     index -= 1
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "select ITEM_DESC from SYS_FORM_ITEM where FORM_ID = 2"
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        #self.tableWidget.setRowCount(0)
        print(records)
        for row_number, row_data in enumerate(records):
            self.w1.insertRow(row_number)
            print(row_data)
            for column_number, data in enumerate(row_data):
                print(data)
                self.w1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        #self.w1.setItem(0, 0, QTableWidgetItem("Name"))
        connection.close()