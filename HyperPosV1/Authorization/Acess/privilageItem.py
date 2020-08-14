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

        #7

    def showMessageBox(self, title, message):
        msgbox = QtWidgets.QMessageBox()
        msgbox.setIcon( QtWidgets.QMessageBox.Warning )
        msgbox.setWindowTitle( title )
        msgbox.setText( message )
        msgbox.setStandardButtons( QtWidgets.QMessageBox.Ok )
        msgbox.exec_()

    def FN_LOAD_CREATE(self):
        loadUi('../Presentation/createPrivilageItem.ui', self)
        self.BTN_createPrivItem.clicked.connect(self.FN_CREATE_PRIVILAGE_ITEM)
        self.FN_GET_PRIV()
        self.FN_GET_FORMS()
        self.CMB_priv.currentIndexChanged.connect(self.FN_GET_FORMS)
        self.CMB_form.currentIndexChanged.connect(self.FN_GET_FORMID)
        self.CMB_formItem.currentIndexChanged.connect(self.FN_GET_ITEMID)
        self.CMB_status.addItems(["0", "1"])
        self.FN_GET_FORMID()
        self.FN_GET_ITEMID()

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
        self.CMB_form.clear()
        self.priv=self.CMB_priv.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql = "SELECT FORM_DESC FROM SYS_FORM as f INNER join SYS_PRIVILEGE  as p on f.FORM_ID = p.FORM_ID WHERE p.PRIV_ID = "+self.priv
        #print(sql)
        mycursor.execute(sql)
        records = mycursor.fetchall()
        if mycursor.rowcount > 0:
            for row in records:
                self.CMB_form.addItems([row[0]])


        connection.close()
        mycursor.close()
        self.FN_GET_ITEMS()

    def FN_GET_ITEMS(self):
        self.CMB_formItem.clear()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        self.form = self.CMB_form.currentText()
        sql_select_query = "select ITEM_DESC , ITEM_STATUS from SYS_FORM_ITEM as i inner join SYS_FORM as f on " \
                           "i.FORM_ID = f.FORM_ID " \
                           "where FORM_DESC = '" + self.form +"'"
        #print(sql_select_query)
        mycursor.execute(sql_select_query)
        records = mycursor.fetchall()
        if mycursor.rowcount > 0:
            for row in records:
                self.CMB_formItem.addItems([row[0]])

        connection.close()
        mycursor.close()

    def FN_GET_FORMID(self):
        self.form = self.CMB_form.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT FORM_ID FROM SYS_FORM WHERE FORM_DESC = '"+self.form+"'"

        mycursor.execute(sql_select_query)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formId.setText(myresult[0])

        connection.close()
        mycursor.close()

    def FN_GET_ITEMID(self):
        self.item = self.CMB_formItem.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "SELECT ITEM_ID FROM SYS_FORM_ITEM WHERE ITEM_DESC = '"+ self.item+"'"

        mycursor.execute(sql_select_query)

        myresult = mycursor.fetchone()
        if mycursor.rowcount > 0:
            self.LB_formItemId.setText(myresult[0])

        connection.close()
        mycursor.close()



    def FN_CREATE_PRIVILAGE_ITEM(self):
        #self.name = self.LE_name.text()
        #self.desc= self.LE_DESC.text()
        self.priv = self.CMB_priv.currentText()
        self.form = self.LB_formId.text()
        self.formItem = self.LB_formItemId.text()
        self.status = self.CMB_status.currentText()
        try:
            connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
            mycursor = connection.cursor()

            sql = "INSERT INTO SYS_PRIVILEG_ITEM (PRIV_ID, FORM_ID,ITEM_ID,ITEM_STATUS)         " \
                  "VALUES ( %s, %s, %s, %s)"

            val = (self.priv, self.form, self.formItem, self.status)
            mycursor.execute( sql, val )
            connection.commit()

            print( mycursor.rowcount, "record inserted." )
            connection.close()
            mycursor.close()
            self.close()
        except mysql.connector.Error as err:
            print( "Something went wrong: {}".format( err ) )
            self.showMessageBox( "Error", "Duplicate Entry" )
            connection.close()
            mycursor.close()



