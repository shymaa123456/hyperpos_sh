import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_formItem(QtWidgets.QDialog):

    def __init__(self):
        super(CL_formItem, self).__init__()

    def FN_DISPLAY_ITEMS (self):
        loadUi('../Presentation/displayFormItems.ui', self)
        self.BTN_getFormItem.clicked.connect(self.FN_DISPLAY_FORM_ITEMS)
        self.CMB_formId.currentIndexChanged.connect(self.FN_GET_FORMNAME)
        self.FN_GET_FORMS()
        self.FN_GET_FORMNAME()




    def FN_DISPLAY_FORM_ITEMS(self):
        self.w1.clear()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        self.form = self.CMB_formId.currentText()

        sql_select_query = "select ITEM_DESC , ITEM_STATUS from SYS_FORM_ITEM where FORM_ID = '"+self.form+"'"

        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        for row_number, row_data in enumerate(records):
            self.w1.insertRow(row_number)

            for column_number, data in enumerate(row_data):

                self.w1.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        # self.w1.setItem(0, 0, QTableWidgetItem("Name"))
        connection.close()

    def FN_LOAD_CREATE(self):
        loadUi('../Presentation/createFormItem.ui', self)
        self.BTN_createFormItem.clicked.connect(self.FN_CREATE_FORM_ITEM)
        self.CMB_formItemStatus.addItems(["0","1"])
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.FN_GET_FORMS()
        self.FN_GET_FORMID()

    def FN_LOAD_MODIFY(self):
        loadUi('../Presentation/modifyFormItem.ui', self)


        self.BTN_modifyFormItem.clicked.connect(self.FN_MODIFY_FORM)
        self.CMB_formItemStatus.addItems(["0", "1"])

        self.CMB_formItemName.currentIndexChanged.connect(self.FN_GET_FORM_ITEM)
        self.CMB_formName.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.FN_GET_FORMItems()
        self.FN_GET_FORM_ITEM()

    def FN_GET_FORMS(self):
        self.CMB_formName.clear()
        self.item=  self.LB_formItemID.text()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()

        mycursor.execute("SELECT FORM_DESC FROM SYS_FORM as f  inner join SYS_FORM_ITEM as i on f.FORM_ID=i.FORM_ID"
                         " WHERE i.ITEM_ID = '"+self.item+"' order by f.FORM_ID asc")
        records = mycursor.fetchall()
        for row in records:
            self.CMB_formName.addItems([row[0]])
        connection.close()
        mycursor.close()

    def FN_GET_FORMID(self):
        self.form= self.CMB_formName.currentText()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formID.setText(myresult[0])

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
        self.LB_formItemID.setText(myresult[0])

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

        mycursor.execute("SELECT ITEM_DESC FROM SYS_FORM_ITEM order by FORM_ID asc")
        records = mycursor.fetchall()

        for row in records:

            self.CMB_formItemName.addItems([row[0]])


        connection.close()
        mycursor.close()
    def FN_GET_FORM_ITEM(self):
        self.FN_GET_FORMITEMID()
        self.id = self.LB_formItemID.text()
        self.FN_GET_FORMS()
        self.FN_GET_FORMID()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "select * from SYS_FORM_ITEM where ITEM_ID = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()

        self.LE_desc.setText(record[2])
        self.CMB_formName.setCurrentText(record[1])

        self.CMB_formItemStatus.setCurrentText(record[3])

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_FORM(self):
        self.id = self.LB_formItemID.text()
        self.form = self.LB_formID.text()
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