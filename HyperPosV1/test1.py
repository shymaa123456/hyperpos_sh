

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from PyQt5 import QtCore
import mysql.connector
if __name__ == '__main__':

    connection = mysql.connector.connect(host='localhost', database='PosDB'
                                         , user='root', password='password', port='3306')
    #        sql_select_Query = "select * from Hyperpos_users where name = '" + username +"' and password = '"+ password+"'"

    sql_select_Query = "select * from Hyperpos_users where name = 'mustafa' and password = '123'"

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    if cursor.rowcount > 0:

        # save the login in the table

       print('connected')

    else:

        print("Please Enter Correct Username and Password")

