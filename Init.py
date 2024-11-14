import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import front
import back1#TEST

#UI Loading
Init_Class = uic.loadUiType("front/UI/Init.ui")[0]

#메인윈도우 설정    
class MainWindow(QMainWindow, Init_Class) :
#variables
    totalPrice = 0
    
    def Reset_lcd_Price(self) :
        self.lcd_Price.display(self.totalPrice)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_setting()

    #Initial_settings (execute once)
    def init_setting(self) :
        #Timer_Init
        self.timer = front.timeoutClass(self)
        self.lcd_Timer.display(180)

        #CartList_Init
        self.cartList = self.cartListWidget

        #MenuList_Init
        self.menuList = self.menuListWidget
        #print("log_1" + str(self))
        front.menuWidget_Load(self, 'ALL')

        self.set_MainPage_Index(0)

    #need to change def name
    def add_timer(self) :
        self.timer.remain_Time += self.timer.add_Time
        self.lcd_Timer.display(self.timer.remain_Time)

    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

#Move_Page/화면 전환(stackedWidget 관련)
    #move to initPage
    def mainPage_toInit(self) :
        try :
            self.timer.timeout_Stop()
            self.set_MainPage_Index(0)
        except : 
            self.set_MainPage_Index(0)

    #move to selectPage
    def mainPage_toSelect(self) :
        self.set_MainPage_Index(1)
        front.btn_CartListClear(self)

    #move to defaultMenuPage
    def mainPage_toDefault(self) :
        self.lcd_Timer.display(180)
        self.timer.timeout_Start(self.timer.timeout_Time)
        self.set_MainPage_Index(2)

    #move to voiceOrderPage
    def mainPage_toVoice(self) :
        self.set_MainPage_Index(3)
#Move_Page

#btn_MenuType/메뉴종류 설정('ALL', '디카페인', '커피', '티(음료)', '디저트')
    def btn_MenuALL(self) :
        front.menuWidget_Load(self, 'ALL')
        
    def btn_MenuCoffee(self) :
        front.menuWidget_Load(self, '커피')
        
    def btn_MenuDeCaffeine(self) :
        front.menuWidget_Load(self, '디카페인')
        
    def btn_MenuDrinks(self) :
        front.menuWidget_Load(self, '티')
        
    def btn_MenuDessert(self) :
        front.menuWidget_Load(self, '디저트')
        
#btn_MenuType

#btn_ETC/기타 버튼
    def btn_CartListClear(self) :
        front.btn_CartListClear(self)

#btn_ETC

######################################################

    def btnTEST(self) :
        pass

######################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()