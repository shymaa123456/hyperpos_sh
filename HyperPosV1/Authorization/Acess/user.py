import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector


class CL_user(QtWidgets.QDialog):

    def __init__(self):
        super(CL_user, self).__init__()





    def FN_LOAD_MODIFY(self):
        loadUi('../Presentation/modifyUser.ui', self)
        self.FN_GET_USERS()
        self.FN_GET_USERID()
        self.FN_GET_USER()
        self.CMB_userName.currentIndexChanged.connect( self.FN_GET_USER )
        self.BTN_modifyUser.clicked.connect(self.FN_MODIFY_USER)
        self.CMB_branch.addItems(["1", "2", "3"])
        self.CMB_userType.addItems(["1", "2", "3"])
        self.CMB_userStatus.addItems(["0", "1"])
    def FN_LOAD_CREATE(self):

        loadUi('../Presentation/createUser.ui', self)
        self.setWindowTitle('Users')
        self.BTN_createUser.clicked.connect(self.FN_CREATE_USER)

        self.CMB_branch.addItems(["1","2","3"])
        self.CMB_userType.addItems(["1","2","3"])
        self.CMB_userStatus.addItems(["0","1"])
    def FN_GET_USER(self):
        self.FN_GET_USERID()
        self.id = self.LB_userID.text()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query = "select * from SYS_USER where user_id = %s"
        x = (self.id,)
        mycursor.execute(sql_select_query, x)
        record = mycursor.fetchone()
        print(record)
        self.LE_name.setText(record[2])
        self.LE_fullName.setText(record[4])
        self.LE_hrId.setText(record[5])
        self.CMB_branch.setCurrentText(record[1])
        self.CMB_userType.setCurrentText(record[11])
        self.CMB_userStatus.setCurrentText(record[10])

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record retrieved.")

    def FN_MODIFY_USER(self):
        self.id = self.LE_id.text()
        self.name = self.LE_name.text()
        self.password = self.LE_password.text()
        self.branch = self.CMB_branch.currentText()
        self.fullName = self.LE_fullName.text()
        self.hrId = self.LE_hrId.text()
        self.userType = self.CMB_userType.currentText()
        self.status = self.CMB_userStatus.currentText()

        #         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')

        mycursor = connection.cursor()

        changeDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        sql = "UPDATE SYS_USER   set USER_NAME= %s ,  USER_PASSWORD= %s  ,  BRANCH_NO = %s, USER_FULLNAME = %s , USER_HR_ID = %s, USER_CHANGED_ON = %s , USER_CHENGED_BY = %s, USER_STATUS = %s, USER_TYPE_ID = %s where USER_id= %s "
        val = (self.name  , self.password, self.branch, self.fullName,self.hrId, changeDate, '', self.status, self.userType , self.id)
        print(val)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record Modified.")

        self.close()

    def FN_GET_USERS(self):

        connection = mysql.connector.connect( host='localhost', database='PosDB'
                                              , user='root', password='password', port='3306' )
        mycursor = connection.cursor()

        mycursor.execute( "SELECT USER_NAME FROM SYS_USER order by USER_ID asc" )
        records = mycursor.fetchall()
        for row in records:
            self.CMB_userName.addItems( [row[0]] )

        connection.commit()
        connection.close()
        mycursor.close()
    def FN_GET_USERID(self):
        self.user = self.CMB_userName.currentText()
        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        sql_select_query= "SELECT USER_ID FROM SYS_USER WHERE USER_NAME = %s"
        x = (self.user,)
        mycursor.execute(sql_select_query, x)
        myresult = mycursor.fetchone()
        self.LB_userID.setText(myresult [0])

    def FN_CREATE_USER(self):
        self.name = self.LE_name.text()
        self.password = self.LE_password.text()
        self.branch = self.CMB_branch.currentText()
        self.fullName = self.LE_fullName.text()
        self.hrId = self.LE_hrId.text()
        self.userType = self.CMB_userType.currentText()
        self.status = self.CMB_userStatus.currentText()

        connection = mysql.connector.connect(host='localhost', database='PosDB'
                                             , user='root', password='password', port='3306')
        mycursor = connection.cursor()
        # get max userid
        mycursor.execute("SELECT max(USER_ID) FROM SYS_USER")
        myresult = mycursor.fetchone()

        if myresult[0] == None:
            self.id = "1"
        else:
            self.id = int(myresult[0]) + 1

        creationDate = str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))

        print(creationDate)

        sql = "INSERT INTO SYS_USER (USER_ID, BRANCH_NO, USER_NAME, USER_PASSWORD, USER_FULLNAME, USER_HR_ID, USER_CREATED_ON, USER_CREATED_BY, USER_CHANGED_ON, USER_CHENGED_BY,USER_STATUS, USER_TYPE_ID)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"

        # sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (
        self.id, self.branch, self.name, self.password, self.fullName, self.hrId, creationDate, '', '', '', self.status,
        self.userType)
        mycursor.execute(sql, val)
        # mycursor.execute(sql)
        connection.commit()

        connection.close()
        mycursor.close()

        print(mycursor.rowcount, "record inserted.")

        self.close()
