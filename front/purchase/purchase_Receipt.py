from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

Order_Class = uic.loadUiType("front/purchase/purchase_Receipt.ui")[0]

class purchaseWindow(QDialog, Order_Class) :
    def __init__(self, orderList, parent) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()
        self.parent_mainWindow = parent

        i = 0
        for items in orderList :
            strItem = items[0] + '::' + '-'.join(items[1]) + '::' + str(items[2]) + '::' + str(items[3])
            self.purchaseListWidget.insertItem(i, strItem)
            i += 1

    #창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    #창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def purchaseWindow_Close(self) :
        #print(self.parent_mainWindow)
        self.parent_mainWindow.timer.timeout_Resume(self.parent_mainWindow.timer.remain_Time)
        self.close()
    #Buttons