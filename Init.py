import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import Front
import data_query

#UI Loading
Init_Class = uic.loadUiType("Front/UI/Init.ui")[0]

#init_setting
totalPrice = 0
totalPrice = 123456 #TEST

menuItemNums = 8
db = data_query.menu_price_path()

#메인윈도우 설정
class MainWindow(QMainWindow, Init_Class) :
#variables
    timeoutTime = 3 * 60
    menuIndex = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_setting()

    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

    #기초 세팅값 설정
    def init_setting(self) :
        self.setup_MenuList()
        self.lcd_Timer.display(180)
        self.set_MainPage_Index(0)

    #timeOut
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
            timeoutMsgbox = Front.timeoutMsgBox()
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
    #timeOut END

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
            checkOrder_Window = Front.OrderWindow()
            checkOrder_Window.order_Price.display(totalPrice)
            checkOrder_Window.showModal()

        else :
            #아무것도 주문하지 않았을 시 알림창
            pass

    #menuList
    def setup_MenuList(self) :
        self.load_MenuList()
    
    def load_MenuList(self) :
        i = 0
        db = Front.db

        for item in db[self.menuIndex:self.menuIndex + 8] :
            imgPath = item[2]
            menuPrice = item[1] #Do not Delete

            menuStr = 'self.menuWidget_'+str(i)+'.setMenuItem("'+imgPath+'", menuPrice)'
            eval(menuStr)

            i += 1
    
    def reset_MenuList(self) :
        for i in range(1, 8) :
            menuStr = 'self.menuWidget_'+str(i)+'.setMenuItemDefault()'
            eval(menuStr)

    def btn_MenuPrev(self) :
        self.menuIndex -= 8
        self.reset_MenuList()
        self.load_MenuList()

        if self.menuIndex == 0 :
            self.btn_menuPrev.setDisabled(True)
        if self.menuIndex + 8 < len(Front.db) :
            self.btn_menuNext.setEnabled(True)
    
    def btn_MenuNext(self) :
        self.menuIndex += 8
        self.reset_MenuList()
        self.load_MenuList()

        if self.menuIndex != 0 :
            self.btn_menuPrev.setEnabled(True)
        if self.menuIndex + 8 > len(Front.db) :
            self.btn_menuNext.setDisabled(True)
    #menuList END

#프로그램 시작
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()