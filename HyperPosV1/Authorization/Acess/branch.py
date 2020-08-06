
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic ,QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error
from datetime import datetime
import mysql.connector

class CL_user(QtWidgets.QDialog):
    

    def __init__(self):
        super(CL_user, self).__init__()
        loadUi('../Presentation/Branch.ui', self)
        self.btn_create_branch.clicked.connect(self.fn_create_branch)
        self.cmb_branch_id.addItems(["1","2","3"])
        self.cmb_branch_status.addItems(["0","1"])
               
    def fn_create_branch(self):
         self.branchId = self.CMB_branchId.currentText()
         self.branchCompany = self.QLE_branchCompany.text()
         self.branchDescA = self.QLE_branchDescA.text()
         self.branchDescE = self.QLE_branchDescE.text()
         self.branchAddress = self.QLE_branchAddress.text()
         self.branchCity = self.QLE_branchCity.text()
         self.branchTel1 = self.QLE_branchTel1.text()
         self.branchTel2 = self.QLE_branch_tel2.text()
         self.branchFax = self.QLE_branch_fax.text()
         self.branchEmail = self.QLE_branchEmail.text()
         self.branchNotes = self.QLE_branchNotes.text()
         self.branchChangedOn = self.QLE_branchChangedOn.text()
         self.branchCurrency = self.QLE_branchCurrency.text()
         self.branchNotes = self.QLE_branchNotes.text()
         self.branchStatus = self.CMB_branch_status.currentText()
   
#         connection = mysql.connector.connect(host='localhost',database='test',user='shelal',password='2ybQvkZbNijIyq2J',port='3306')
         connection = mysql.connector.connect(host='localhost',database='PosDB'
                                          ,user='root',password='password',port='3306')
         mycursor = connection.cursor()
         #get max userid
         mycursor.execute("SELECT max(USER_ID) FROM SYS_USER")
         myresult = mycursor.fetchone()

         self.id=int(myresult[0])+1
         
         creationDate=str(datetime.today().strftime('%Y-%m-%d-%H:%M-%S'))
         
         print(creationDate)
         
         sql = "INSERT INTO SYS_USER (BRANCH_NO, BRANCH_COMPANY, BRANCH_DESC_A, BRANCH_DESC_E, BRANCH_ADDRESS, BRANCH_CITY, BRANCH_TEL1, BRANCH_TEL2, BRANCH_FAX, BRANCH_EMAIL,BRANCH_NOTES, BRANCH_CHANGED_ON,BRANCH_CURRENCY, BRANCH_STATUS)         VALUES ( %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
         
         #sql = "INSERT INTO SYS_USER (USER_ID,USER_NAME) VALUES (%s, %s)"
         val = (self.branchId, self.branchCompany,self.name,self.password,self.fullName,self.hrId,creationDate,'','','',self.status,self.userType)
         mycursor.execute(sql, val)
         #mycursor.execute(sql)
         connection.commit()
    
         connection.close()
         mycursor.close()
         
            
         print(mycursor.rowcount, "record inserted.")
 