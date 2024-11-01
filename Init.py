import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import Front
#import data_query

#UI Loading
Init_Class = uic.loadUiType("Front/UI/Init.ui")[0]

#init_setting
totalPrice = 0
totalPrice = 123456 #TEST

menuItemNums = 8

#메인윈도우 설정
class MainWindow(QMainWindow, Init_Class) :
#variables
    menuIndex = 0
    menuType = 'ALL'
    db = Front.get_db(menuType)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_setting()

    #기초 세팅값 설정
    def init_setting(self) :
        self.timer = Front.timeoutClass(self)
        self.lcd_Timer.display(180)
        self.set_MainPage_Index(0)
        self.setup_MenuList()

    #testAREA
    def add_timer(self) :
        self.timer.remain_Time += self.timer.timeout_Time
        self.lcd_Timer.display(self.timer.remain_Time)
    #testAREA_END

    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

#Buttons
    #(시작화면)으로 이동
    def mainPage_toInit(self) :
        try :
            self.timer.timeout_Stop()
            self.set_MainPage_Index(0)
            self.setup_MenuList()
        except : 
            self.set_MainPage_Index(0)
            self.setup_MenuList()

    #(일반주문, 음성주문 선택화면)으로 이동
    def mainPage_toSelect(self) :
        self.set_MainPage_Index(1)

    #(일반주문화면)으로 이동
    def mainPage_toDefault(self) :
        self.lcd_Timer.display(180)
        self.timer.timeout_Start(self.timer.timeout_Time)
        self.set_MainPage_Index(2)

    #(음성주문화면)으로 이동
    def mainPage_toVoice(self) :
        self.set_MainPage_Index(3)

    #(결제창)으로 이동
    def popup_checkOrder(self) :
        if totalPrice > 0 :
            #timer pause/resume
            self.timer.timeout_Pause()

            #Open New Window/ApplicationModal
            checkOrder_Window = Front.OrderWindow(self)
            checkOrder_Window.order_Price.display(totalPrice)
            checkOrder_Window.showModal()

        else :
            #아무것도 주문하지 않았을 시 알림창
            pass

    #menuList
    def setup_MenuList(self) :
        self.menuIndex = 0
        self.menuType = 'ALL'
        self.load_MenuList(self.menuType)
    
    def load_MenuList(self, menuType) :
        self.reset_MenuList()
        i = 0

        db = Front.get_db(menuType)

        if self.menuIndex == 0 :
            self.btn_menuPrev.setDisabled(True)
        else :
            self.btn_menuPrev.setEnabled(True)

        if self.menuIndex + 8 < len(db) :
            self.btn_menuNext.setEnabled(True)
        else :
            self.btn_menuNext.setDisabled(True)

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
        self.load_MenuList(self.menuType)
    
    def btn_MenuNext(self) :
        self.menuIndex += 8
        self.load_MenuList(self.menuType)

    #menuList END

    #btnMenu

    def btn_MenuALL(self) :
        self.menuIndex = 0
        self.menuType = 'ALL'
        self.load_MenuList(self.menuType)
    
    def btn_MenuCoffee(self) :
        self.menuIndex = 0
        self.menuType = 'Coffee'
        self.load_MenuList(self.menuType)

    def btn_MenuDeCaffeine(self) :
        self.menuIndex = 0
        self.menuType = 'DeCaffeine'
        self.load_MenuList(self.menuType)

    def btn_MenuDrinks(self) :
        self.menuIndex = 0
        self.menuType = 'Drinks'
        self.load_MenuList(self.menuType)

    def btn_MenuDessert(self) :
        self.menuIndex = 0
        self.menuType = 'Dessert'
        self.load_MenuList(self.menuType)


#프로그램 시작
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()