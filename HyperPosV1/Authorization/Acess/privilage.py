import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_privilage(QtWidgets.QDialog):

    def __init__(self):
        super(CL_privilage, self).__init__()

        #


    def FN_LOAD_CREATE(self):
        loadUi('../Presentation/createPrivilage.ui', self)
        self.BTN_createPrivilage.clicked.connect(self.FN_CREATE_PRIVILAGE)
        self.FN_GET_ROLES()
        self.FN_GET_FORMS()
        self.FN_GET_ACTIONS()
        self.FN_GET_ROLENAME()
        self.FN_GET_FORMNAME()
        self.FN_GET_ACTIONNAME()
        self.CMB_roleId.currentIndexChanged.connect(self.FN_GET_ROLENAME)
        self.CMB_formId.currentIndexChanged.connect(self.FN_GET_FORMNAME)
        self.CMB_actionId.currentIndexChanged.connect(self.FN_GET_ACTIONNAME)
    def FN_LOAD_MODFIY(self):
        loadUi('../Presentation/modifyPrivilage.ui', self)
        self.BTN_getPrivilage.clicked.connect(self.FN_GET_PRIV)
        self.BTN_modifyPrivilage.clicked.connect(self.FN_MODIFY_PRIV)
        self.CMB_roleId.currentIndexChanged.connect(self.FN_GET_ROLENAME)
        self.CMB_formId.currentIndexChanged.connect(self.FN_GET_FORMNAME)
        self.CMB_actionId.currentIndexChanged.connect(self.FN_GET_ACTIONNAME)
    def FN_GET_ACTIONS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ACTION_ID FROM SYS_PRINT_EXPORT_LOOKUP order by ACTION_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_actionId.addItems([row[0]])


        connection.close()
        mycursor.close()
    def FN_GET_ROLES(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ROLE_ID FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleId.addItems([row[0]])


        connection.close()
        mycursor.close()

    def FN_GET_FORMS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT FORM_ID FROM SYS_FORM order by FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formId.addItems([row[0]])


        connection.close()
        mycursor.close()


    def FN_GET_ROLENAME(self):
        self.role = self.CMB_roleId.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ROLE_NAME FROM SYS_ROLE WHERE ROLE_ID = %s"
        x = (self.role,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_roleName.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_FORMNAME(self):
        self.form = self.CMB_formId.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_DESC FROM SYS_FORM WHERE FORM_ID = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_formName.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_ACTIONNAME(self):
        self.action = self.CMB_actionId.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ACTION_DESC FROM SYS_PRINT_EXPORT_LOOKUP WHERE ACTION_ID = %s"
        x = (self.action,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_actionName.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_PRIV(self):

        self.id = self.LE_id.text()
        self.FN_GET_ROLES()
        self.FN_GET_FORMS()
        self.FN_GET_ACTIONS()
        self.FN_GET_ROLENAME()
        self.FN_GET_FORMNAME()
        self.FN_GET_ACTIONNAME()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "select * from SYS_PRIVILEGE where PRIV_ID = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()

        self.CMB_roleId.setCurrentText(record[1])
        self.CMB_formId.setCurrentText(record[2])
        self.CMB_actionId.setCurrentText(record[3])

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")
    def FN_MODIFY_PRIV(self):
        self.id = self.LE_id.text()
        self.role = self.CMB_roleId.currentText()
        self.form = self.CMB_formId.currentText()
        self.action = self.CMB_actionId.currentText()

        #         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')

        mycursor = connection.cursor()


        sql = "UPDATE SYS_PRIVILEGE  set PRIV_ID= %s ,  FORM_ID= %s  ,  ACTION_ID= %s  where PRIV_ID= %s "

        val = (self.role , self.form,   self.action, self.id)

        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record Modified.")

        self.close()

    def FN_CREATE_PRIVILAGE(self):
        #self.name = self.LE_name.text()
        #self.desc= self.LE_DESC.text()

        self.role = self.CMB_roleId.currentText()
        self.form = self.CMB_formId.currentText()
        self.action = self.CMB_actionId.currentText()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        # get max userid
        mycursor.execute("SELECT max(PRIV_ID) FROM SYS_PRIVILEGE")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1


        sql = "INSERT INTO SYS_PRIVILEGE (PRIV_ID, ROLE_ID,FORM_ID,ACTION_ID)         " \
              "VALUES ( %s, %s, %s, %s)"

        val = (self.id, self.role, self.form,   self.action)
        mycursor.execute(sql, val)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record inserted.")

        self.close()
