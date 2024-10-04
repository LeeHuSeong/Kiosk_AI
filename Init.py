import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import Purchase

#UI Loading
Init_Class= uic.loadUiType("Init.ui")[0]

#메인윈도우 설정
class MainWindow(QMainWindow, Init_Class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mainPage_toInit()

#def
    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

#180초 타이머 설정
    def timeout_Start(self) :
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.remaining_time = 5

    def timeout_Return(self) :
        QMessageBox.about(self, 'test2', 'test2')
        self.set_MainPage_Index(0)

    def update_timer(self) :
        if self.remaining_time > 0 :
            self.remaining_time -= 1
            self.lcd_Timer.display(self.remaining_time)
        else :
            self.timer.stop()
            self.timeout_Return()
        
#Buttons
    #(시작화면)으로 이동
    def mainPage_toInit(self) :
        self.set_MainPage_Index(0)

    #(일반주문, 음성주문 선택화면)으로 이동
    def mainPage_toSelect(self) :
        self.set_MainPage_Index(1)

    #(일반주문화면)으로 이동
    def mainPage_toDefault(self) :
        self.timeout_Start()
        self.set_MainPage_Index(2)

    #(음성주문화면)으로 이동
    def mainPage_toVoice(self) :
        self.set_MainPage_Index(3)

    #(결제창)으로 이동
    def popup_purchaseWindow(self) :
        #Open New Window/ApplicationModal
        self.purchase_Window = Purchase.PurchaseWindow()
        self.purchase_Window.show()

#프로그램 시작
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()