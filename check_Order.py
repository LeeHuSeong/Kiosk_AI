import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

Order_Class = uic.loadUiType("UI/check_Order.ui")[0]

class OrderWindow(QDialog, Order_Class) :
    def __init__(self) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

    #창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    #창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    #Buttons