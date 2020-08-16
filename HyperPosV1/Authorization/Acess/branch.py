
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic ,QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector

class CL_branch(QtWidgets.QDialog):


    def __init__(self):
        super(CL_branch, self).__init__()
        loadUi('../Presentation/Branch.ui', self)
        self.BTN_createBranch.clicked.connect(self.FN_createBranch)
        self.CMB_branchCompany.addItems(["zayed","asher","sphinx"])
        self.CMB_branchStatus.addItems(["0","1"])
        
    def FN_createBranch(self):       
        self.branchCompany = self.CMB_branchCompany.currentText()
        self.branchDescA = self.QLE_branchDescA.text()
        self.branchDescE = self.QLE_branchDescE.text()
        self.branchAddress = self.QLE_branchAddress.text()
        self.branchCity = self.QLE_branchCity.text()
        self.branchTel1 = self.QLE_branchTel1.text()
        self.branchTel2 = self.QLE_branchTel2.text()
        self.branchFax = self.QLE_branchFax.text()
        self.branchEmail = self.QLE_branchEmail.text()
        self.branchNotes = self.QLE_branchNotes.text()
        self.branchChangedOn = self.QLE_branchChangedOn.text()
        self.branchCurrency = self.QLE_branchCurrency.text()
        self.branchStatus = self.CMB_branchStatus.currentText()
   
#         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
        connection = mysql.connector.connect(host='localhost',database='PosDB'
                                         ,user='root',password='password',port='3306')
        mycursor = connection.cursor()
        #get max branch i
        mycursor.execute("SELECT max(CAST(BRANCH_NO as SIGNED)) FROM BRANCH")
        myresult = mycursor.fetchone()
        if len(myresult) == 0:
            self.branchId=1

        else:
            self.branchId=myresult[0]+1
                  

         
        sql = "INSERT INTO BRANCH (BRANCH_NO, BRANCH_COMPANY, BRANCH_DESC_A, BRANCH_DESC_E, BRANCH_ADDRESS, BRANCH_CITY, BRANCH_TEL1, BRANCH_TEL2, BRANCH_FAX, BRANCH_EMAIL,BRANCH_NOTES, BRANCH_CHANGED_ON,BRANCH_CURRENCY, BRANCH_STATUS)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
         
        #sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
        val = (self.branchId, self.branchCompany,self.branchDescA,self.branchDescE,self.branchAddress,self.branchCity,self.branchTel1,self.branchTel2,self.branchFax,self.branchEmail,self.branchNotes,self.branchChangedOn,self.branchCurrency,self.branchStatus)
        mycursor.execute(sql, val)
        #mycursor.execute(sql)
        connection.commit()
    
        connection.close()
        mycursor.close()
         
            
        print(mycursor.rowcount, "record inserted.") 

        self.close()
 