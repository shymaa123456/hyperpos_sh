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
        self.FN_GET_ROLEID()
        self.FN_GET_FORMID()
        self.FN_GET_ACTIONID()
        self.CMB_roleName.currentIndexChanged.connect(self.FN_GET_ROLEID)
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.CMB_actionName.currentIndexChanged.connect(self.FN_GET_ACTIONID)
    def FN_LOAD_MODFIY(self):
        loadUi('../Presentation/modifyPrivilage.ui', self)

        self.LE_id.textChanged.connect(self.FN_GET_PRIV)
        self.BTN_modifyPrivilage.clicked.connect(self.FN_MODIFY_PRIV)
        self.CMB_roleName.currentIndexChanged.connect(self.FN_GET_ROLEID)
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.CMB_actionName.currentIndexChanged.connect(self.FN_GET_ACTIONID)
        # self.FN_GET_ROLEID()
        # self.FN_GET_FORMID()
        # self.FN_GET_ACTIONID()
    def FN_GET_ACTIONS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ACTION_DESC FROM SYS_PRINT_EXPORT_LOOKUP order by ACTION_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_actionName.addItems([row[0]])


        connection.close()
        mycursor.close()
    def FN_GET_ROLES(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ROLE_NAME FROM SYS_ROLE order by ROLE_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_roleName.addItems([row[0]])


        connection.close()
        mycursor.close()

    def FN_GET_FORMS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT FORM_DESC FROM SYS_FORM order by FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formName.addItems([row[0]])


        connection.close()
        mycursor.close()


    def FN_GET_ROLEID(self):
        self.role = self.CMB_roleName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ROLE_ID FROM SYS_ROLE WHERE ROLE_Name = %s"
        x = (self.role,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_roleId.setText(myresult[0])
        connection.close()
        mycursor.close()

    def FN_GET_ROLENAME(self):
        self.role = self.LB_roleId.text()
        connection = mysql.connector.connect( host='localhost', database='PosDB'
                                              , user='root', password='password', port='3306' )
        mycursor = connection.cursor()
        sql_select_query = "SELECT ROLE_DESC FROM SYS_ROLE WHERE ROLE_ID = %s"
        x = (self.role,)
        mycursor.execute( sql_select_query, x )
        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.CMB_roleName.setText( myresult[0] )
        connection.close()
        mycursor.close()

    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formId.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_ACTIONID(self):
        self.action = self.CMB_actionName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ACTION_ID FROM SYS_PRINT_EXPORT_LOOKUP WHERE ACTION_DESC = %s"
        x = (self.action,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_actionId.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_PRIV(self):

        self.id = self.LE_id.text()
        self.FN_GET_ROLES()
        self.FN_GET_FORMS()
        self.FN_GET_ACTIONS()
        # self.FN_GET_ROLEID()
        # self.FN_GET_FORMID()
        # self.FN_GET_ACTIONID()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "select * from SYS_PRIVILEGE where PRIV_ID = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        print(record)
        self.LB_roleId.setText(record[1])
        self.LB_formId.setText(record[2])
        self.LB_actionId.setText(record[3])
       # self.FN_GET_ROLENAME()
        #self.CMB_roleName.setCurrentIndex(self,1)
        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")
    def FN_MODIFY_PRIV(self):
        self.id = self.LE_id.text()
        self.role = self.LB_roleId.text()
        self.form = self.LB_formId.text()
        self.action = self.LB_actionId.text()

        #         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')

        mycursor = connection.cursor()


        sql = "UPDATE SYS_PRIVILEGE  set ROLE_ID= %s ,  FORM_ID= %s  ,  ACTION_ID= %s  where PRIV_ID= %s "

        val = (self.role , self.form,   self.action, self.id)

        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record Modified.")

        self.close()

    def FN_CREATE_PRIVILAGE(self):

        self.role = self.LB_roleId.text()
        self.form = self.LB_formId.text()
        self.action = self.LB_actionId.text()

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
