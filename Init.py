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
    menuIndex = 0
    menuType = 'ALL'
    totalPrice = 0
    #totalPrice = 123456 #will remove

    menuData = front.get_db(menuType)
    optionData = back1.data_query.get_menu_option()

    #cartList
    def Reset_lcd_Price(self) :
        self.lcd_Price.display(self.totalPrice)

        #menuData = [메뉴이름, 옵션딕셔너리, 1, 메뉴 총가격]
    def cartWidget_Add(self, menuData) :
        #print(menuData[1])
        item_Widget = front.cartItem(self.cartList, menuData, self)
        item = QListWidgetItem()
        item.setSizeHint(item_Widget.sizeHint())

        self.cartList.addItem(item)
        self.cartList.setItemWidget(item, item_Widget)
        self.Reset_lcd_Price()
    
    def btn_listWidgetClear(self) :
        self.cartList.clear()
        self.totalPrice = 0
        self.lcd_Price.display(self.totalPrice)
    
    #cartListEnd

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
        self.menuWidget_Load()

        self.set_MainPage_Index(0)

    def menuWidget_Load(self) :
        #[메뉴이름, 가격,이미지경로,카테고리,품절여부(0/1)]
        menuDB = back1.get_menu_price_path_category()
        menuData = []

        for i in range(0, len(menuDB), 4) :
            menuData.append(menuDB[i:i + 4])

        for itemSet in menuData :
            item_Widget = front.menu_ItemSet(self.menuList, itemSet, self)
            item = QListWidgetItem()
            item.setSizeHint(item_Widget.sizeHint())

            self.menuList.addItem(item)
            self.menuList.setItemWidget(item, item_Widget)

    #need to change def name
    def add_timer(self) :
        self.timer.remain_Time += self.timer.timeout_Time
        self.lcd_Timer.display(self.timer.remain_Time)

    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

#Move_Page
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
        self.btn_listWidgetClear()

    #move to defaultMenuPage
    def mainPage_toDefault(self) :
        self.lcd_Timer.display(180)
        self.timer.timeout_Start(self.timer.timeout_Time)
        self.set_MainPage_Index(2)

    #move to voiceOrderPage
    def mainPage_toVoice(self) :
        self.set_MainPage_Index(3)

######################################################

    def btnTEST(self) :
        pass


######################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()