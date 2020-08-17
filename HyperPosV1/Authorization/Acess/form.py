import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_form(QtWidgets.QDialog):

    def __init__(self):
        super(CL_form, self).__init__()

    def FN_LOAD_CREATE(self):
        loadUi('../Presentation/createForm.ui', self)
        self.BTN_createForm.clicked.connect(self.FN_CREATE_FORM)
        self.CMB_formStatus.addItems(["0","1"])

    def FN_LOAD_MODIFY(self):
        loadUi('../Presentation/modifyForm.ui', self)

        self.FN_GET_FORMS()
        self.FN_GET_FORMID()
        self.FN_GET_FORM()
        self.CMB_formName.currentIndexChanged.connect( self.FN_GET_FORM )
        self.BTN_modifyForm.clicked.connect(self.FN_MODIFY_FORM)
        self.CMB_formStatus.addItems(["0", "1"])
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
    def FN_GET_FORMID(self):
        self.form = self.CMB_formName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = %s"
        x = (self.form,)
        mycursor.execute(sql_select_query, x)

        myresult = mycursor.fetchone()
        self.LB_formID.setText(myresult[0])

        connection.close()
        mycursor.close()
    def FN_GET_FORM(self):
        self.FN_GET_FORMID()
        self.id = self.LB_formID.text()

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
        self.id = self.LB_formID.text()
        self.desc = self.LE_desc.text()
        self.type = self.LE_type.text()
        self.status = self.CMB_formStatus.currentText()
        self.help = self.LE_help.text()

        #connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')

        mycursor = connection.cursor()

        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        sql = "UPDATE SYS_FORM  set FORM_DESC= %s ,FORM_TYPE= %s  , FORM_STATUS = %s, FORM_HELP = %s where FORM_id= %s "

        val = (self.desc  , self.type, self.status, self.help, self.id)

        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record Modified.")

        self.close()

    def FN_CREATE_FORM(self):
        self.desc = self.LE_desc.text()

        self.type = self.LE_type.text()
        self.help= self.LE_help.text()

        self.status = self.CMB_formStatus.currentText()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        # get max userid
        mycursor.execute("SELECT max(FORM_ID) FROM SYS_FORM")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1



        sql = "INSERT INTO SYS_FORM (FORM_ID, FORM_DESC, FORM_TYPE,FORM_STATUS,FORM_HELP)  VALUES ( %s, %s, %s, %s,%s)"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (self.id, self.desc, self.type, self.status, self.help)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record inserted.")

        self.close()
