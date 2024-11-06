from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

Order_Class = uic.loadUiType("front/menu/selectOption.ui")[0]

class OrderWindow(QDialog, Order_Class) :
    def __init__(self, menuData, optionData) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        #self.parent_mainWindow = parent

        #UI관련사항
        #각각의 옵션을 위젯으로 구성 
        # ex) 샷추가Widget(없음버튼, 1샷추버튼, 2샷추버튼)

    #창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    #창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())