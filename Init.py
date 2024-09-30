import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

#UI Loading
form_class = uic.loadUiType("Init.ui")[0]

#메인윈도우 설정
class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mainPage.setCurrentIndex(0)

#Buttons
    #(시작화면)으로 이동
    def btn_ToInitPage(self) :
        self.mainPage.setCurrentIndex(0)
    #(일반주문, 음성주문 선택화면)으로 이동
    def btn_ToSelectPage(self) :
        self.mainPage.setCurrentIndex(1)
    #(일반주문화면)으로 이동
    def btn_ToDefaultMenuPage(self) :
        self.mainPage.setCurrentIndex(2)
    #(음성주문화면)으로 이동
    def btn_ToVoiceOrderPage(self) :
        self.mainPage.setCurrentIndex(3)
    #(결제창)으로 이동
    def btn_ToOrderPage(self) :
        pass

#프로그램 시작
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()

##Commit Test 