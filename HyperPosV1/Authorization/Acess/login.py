#!/usr/bin/env python3
# -*     - coding: utf-8 -*-
"""
Created on Mon Jun 29 19:52:06 2020

@author: emad
"""


import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from PyQt5 import QtCore
#import Controller
from main import CL_main
from user import CL_user
import mysql.connector
#hi i am writing a comment
from Role import CL_role
from form import CL_form
from privilage import CL_privilage


class CL_login(QtWidgets.QDialog):
    switch_window = QtCore.pyqtSignal()
   
    def FN_login(self):

        if len(self.LE_userName.text()) > 0 and len(self.LE_password.text()) > 0:                                                                                
            print("Login!")
            self.username = self.LE_userName.text()
            self.password = self.LE_password.text()
            self.LE_userName.clear()
            self.LE_password.clear()
            self.FN_loadData(self.username,self.password)
            
        else:

            QtWidgets.QMessageBox.warning(self, "Error", "Please enter your Username and Password")
            print("Please enter your Username and Password")


    def FN_loadData(self, username, password):
     try:
#        connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
#    
        connection = mysql.connector.connect(host='localhost',database='PosDB'
                                          ,user='root',password='password',port='3306')
#        sql_select_Query = "select * from Hyperpos_users where name = '" + username +"' and password = '"+ password+"'"
    
        sql_select_Query = "select * from Hyperpos_users where name = '" + username +"' and password = '"+ password+"'"
                
        
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        
        if cursor.rowcount >0:
            
            #save the login in the table 
            
            self.switch_window.emit() 
           
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Incorrect Username and Password")
            print("Please Enter Correct Username and Password")

     except Error as e:
        print("Error reading data from MySQL table", e)
     finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    def __init__(self):
        super(CL_login, self).__init__()
        loadUi('../Presentation/login.ui', self)
        self.setWindowTitle('HyperPOS Login Page')
        self.LE_userName.setText("mustafa")
        self.LE_password.setText("123")
        self.pixmap = QPixmap("../Presentation/hyperonelogo.png")
        self.label_logo.setPixmap(self.pixmap)
        self.btn_login.clicked.connect(self.FN_login)


class CL_controller():
    def __init__(self):
        pass

    def FN_show_login(self):
        self.login = CL_login()
#        self.user = self.login.username
        self.login.switch_window.connect(self.FN_show_main)
        self.login.show()

    def FN_show_main(self):
        self.window = CL_main()

        self.login.close()
        self.window.show()
def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = CL_controller()
    controller.FN_show_login()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
  
