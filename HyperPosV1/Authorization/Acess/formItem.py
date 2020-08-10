import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_formItem(QtWidgets.QDialog):

    def __init__(self):
        super(CL_formItem, self).__init__()

    def FN_LOAD_CREATE(self):
        loadUi('../Presentation/createFormItem.ui', self)
        self.BTN_createFormItem.clicked.connect(self.FN_CREATE_FORM_ITEM)
        self.CMB_formItemStatus.addItems(["0","1"])
        self.CMB_formId.currentIndexChanged.connect(self.FN_GET_FORMNAME)
        self.FN_GET_FORMS()
        self.FN_GET_FORMNAME()

    def FN_LOAD_MODIFY(self):
        loadUi('../Presentation/modifyFormItem.ui', self)
        self.BTN_getFormItem.clicked.connect(self.FN_GET_FORM_ITEM)
        self.BTN_modifyFormItem.clicked.connect(self.FN_MODIFY_FORM)
        self.CMB_formItemStatus.addItems(["0", "1"])
        self.FN_GET_FORMItems()
        self.CMB_formItemName.currentIndexChanged.connect(self.FN_GET_FORMITEMID)
        self.CMB_formId.currentIndexChanged.connect(self.FN_GET_FORMNAME)
        self.FN_GET_FORMS()
        self.FN_GET_FORMNAME()
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

    def FN_GET_FORMITEMID(self):
        self.item= self.CMB_formItemName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = %s"
        x = (self.item,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_formItemId.setText(myresult[0])

        connection.close()
        mycursor.close()

    def FN_CREATE_FORM_ITEM(self):
        self.desc = self.LE_desc.text()
        self.form = self.CMB_formId.currentText()


        self.status = self.CMB_formItemStatus.currentText()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        # get max userid
        mycursor.execute("SELECT max(ITEM_ID) FROM SYS_FORM_ITEM")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1



        sql = "INSERT INTO SYS_FORM_ITEM (ITEM_ID,FORM_ID,ITEM_DESC, ITEM_STATUS)  VALUES ( %s, %s, %s, %s)"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (self.id,self.form, self.desc,  self.status)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record inserted.")

        self.close()



    def FN_GET_FORMItems(self):
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT ITEM_DESC FROM SYS_FORM_Item order by FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formItemName.addItems([row[2]])


        connection.close()
        mycursor.close()
    def FN_GET_FORM_ITEM(self):

        self.id = self.LB_formItemId.text()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "select * from SYS_FORM where FORM_ID = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        print(record)
        self.LE_desc.setText(record[1])
        self.LE_type.setText(record[2])
        self.LE_help.setText(record[4])

        self.CMB_formStatus.setCurrentText(record[3])

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_FORM(self):
        self.id = self.LB_formItemId.text()
        self.form = self.CMB_formId.currentText()
        self.desc = self.LE_desc.text()
        self.status = self.CMB_formItemStatus.currentText()


        #         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')

        mycursor = connection.cursor()


        sql = "UPDATE SYS_FORM_ITEM  set FORM_ID= %s ,ITEM_DESC= %s  , ITEM_STATUS = %s where ITEM_id= %s "





        val = (self.form  , self.desc, self.status,  self.id)

        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record Modified.")

        self.close()