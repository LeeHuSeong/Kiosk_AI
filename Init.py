import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import check_Order as cO
import timeoutMsgbox as tM

#UI Loading
Init_Class = uic.loadUiType("UI/Init.ui")[0]

totalPrice = 0
totalPrice = 123456 #TEST


#메인윈도우 설정
class MainWindow(QMainWindow, Init_Class) :
#variables
    timeoutTime = 3 #* 60

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_setting()

#def
    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

    #기초 세팅값 설정
    def init_setting(self) :
        self.lcd_Timer.display(180)
        self.set_MainPage_Index(0)

    #180초 타이머 설정
    def timeout_Start(self, timeoutTime) :
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.remaining_time = timeoutTime
        self.lcd_Timer.display(self.remaining_time)

    def timeout_Return(self) :
        self.set_MainPage_Index(0)

    def update_timer(self) :
        if self.remaining_time > 0 :
            self.remaining_time -= 1
            self.lcd_Timer.display(self.remaining_time)
        else :
            self.stop_timer()
            timeoutMsgbox = tM.timeoutMsgBox()
            timeoutMsgbox.showModal()

            timeoutFlag = timeoutMsgbox.timeoutFlag
            if(timeoutFlag == True) :
                timeoutMsgbox.close()
                self.timeout_Return()
            
            else :
                timeoutMsgbox.close()
                self.timeout_Start(self.timeoutTime)

    def add_timer(self) :
        self.remaining_time += self.timeoutTime
        self.lcd_Timer.display(self.remaining_time)

    def pause_timer(self) :
        pass

    def stop_timer(self) :
        self.timer.stop()
        
#Buttons
    #(시작화면)으로 이동
    def mainPage_toInit(self) :
        try :
            self.stop_timer()
            self.set_MainPage_Index(0)
        except : 
            self.set_MainPage_Index(0)

    #(일반주문, 음성주문 선택화면)으로 이동
    def mainPage_toSelect(self) :
        self.set_MainPage_Index(1)

    #(일반주문화면)으로 이동
    def mainPage_toDefault(self) :
        self.lcd_Timer.display(180)
        self.timeout_Start(self.timeoutTime)
        self.set_MainPage_Index(2)

    #(음성주문화면)으로 이동
    def mainPage_toVoice(self) :
        self.set_MainPage_Index(3)

    #(결제창)으로 이동
    def popup_checkOrder(self) :
        if totalPrice > 0 :
            #Open New Window/ApplicationModal
            checkOrder_Window = cO.OrderWindow()
            checkOrder_Window.order_Price.display(totalPrice)
            checkOrder_Window.showModal()

        else :
            #아무것도 주문하지 않았을 시 알림창
            pass

#프로그램 시작
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()