import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_privilageItem(QtWidgets.QDialog):

    def __init__(self):
        super(CL_privilageItem, self).__init__()

        #


    def FN_LOAD_CREATE(self):
        loadUi('../Presentation/createPrivilageItem.ui', self)
        self.BTN_createPrivItem.clicked.connect(self.FN_CREATE_PRIVILAGE_ITEM)
        self.FN_GET_PRIV()
        self.FN_GET_ITEMS()
        self.FN_GET_FORMS()


        self.FN_GET_FORMID()
        self.FN_GET_ITEMID()


        self.CMB_form.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.CMB_formItem.currentIndexChanged.connect(self.FN_GET_ITEMID)
        self.CMB_status.addItems(["0", "1"])
    # def FN_LOAD_MODFIY(self):
    #     loadUi('../Presentation/modifyPrivilage.ui', self)
    #     self.BTN_getPrivilage.clicked.connect(self.FN_GET_PRIV)
    #     self.BTN_modifyPrivilage.clicked.connect(self.FN_MODIFY_PRIV)
    #     self.CMB_roleId.currentIndexChanged.connect(self.FN_GET_ROLENAME)
    #     self.CMB_formId.currentIndexChanged.connect(self.FN_GET_FORMNAME)
    #     self.CMB_actionId.currentIndexChanged.connect(self.FN_GET_ACTIONNAME)
    #
    def FN_GET_PRIV(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT PRIV_ID FROM SYS_PRIVILEGE order by PRIV_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_priv.addItems([row[0]])


        connection.close()
        mycursor.close()

    def FN_GET_FORMS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT FORM_DESC FROM SYS_FORM order by FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_form.addItems([row[0]])


        connection.close()
        mycursor.close()

    def FN_GET_ITEMS(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        self.form = self.CMB_form.currentText()

        sql_select_query = "select ITEM_DESC , ITEM_STATUS from SYS_FORM_ITEM where FORM_ID = '" + self.form + "'"

        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formItem.addItems([row[0]])

        connection.close()
        mycursor.close()

    def FN_GET_FORMID(self):
        self.form = self.CMB_form.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_formId.setText(myresult[0])

        connection.close()
        mycursor.close()

    def FN_GET_ITEMID(self):
        self.item = self.CMB_formItem.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
       # self.LB_formItemId.setText(myresult[0])

        connection.close()
        mycursor.close()



    def FN_CREATE_PRIVILAGE_ITEM(self):
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
