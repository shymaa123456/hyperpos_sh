
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, uic ,QtCore
from PyQt5.QtGui import QPixmap
from mysql.connector import Error

import mysql.connector

from form import CL_form
from user import CL_user
from Authorization.Acess.Role import CL_role
from Authorization.Acess.privilage import CL_privilage


class CL_main(QtWidgets.QMainWindow):
    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        super(CL_main, self).__init__()
        loadUi('../Presentation/main.ui', self)
        self.setWindowTitle('HyperPOS Main Page')
        
        self.QA_Create_User.triggered.connect(self.FN_CREATE_USER)
        self.QA_Modify_User.triggered.connect(self.FN_MODIFY_USER)
        self.QA_Create_Role.triggered.connect(self.FN_CREATE_ROLE)
        self.QA_Modify_Role.triggered.connect(self.FN_MODIFY_ROLE)
        self.QA_Assign_User.triggered.connect(self.FN_ASSIGN)

        self.QA_Create_Priv.triggered.connect(self.FN_CREATE_PRIV)
        self.QA_Modify_Priv.triggered.connect(self.FN_MODIFY_PRIV)
        self.QA_Create_Form.triggered.connect(self.FN_create_form)
        self.QA_Modify_Form.triggered.connect(self.FN_modify_form)

    def FN_actionClicked(self):
        print('Action: ')
        self.switch_window.emit()

    def FN_CREATE_USER(self):
        self.window_two = CL_user()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()
    def FN_MODIFY_USER(self):
        self.window_two = CL_user()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

    def FN_CREATE_ROLE(self):
        self.window_two = CL_role()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()
    def FN_MODIFY_ROLE(self):
        self.window_two = CL_role()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()
DD
    def FN_ASSIGN(self):
        self.window_two = CL_role()
        self.window_two.FN_ASSIGN()
        self.window_two.show()
    def FN_modify_form(self):
        self.window_two = CL_form()
        self.window_two.FN_LOAD_MODIFY()
        self.window_two.show()

    def FN_create_form(self):
        self.window_two = CL_form()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()

    def FN_CREATE_PRIV(self):
        self.window_two = CL_privilage()
        self.window_two.FN_LOAD_CREATE()
        self.window_two.show()
    def FN_MODIFY_PRIV(self):
        self.window_two = CL_privilage()
        self.window_two.FN_LOAD_MODFIY()
        self.window_two.show()