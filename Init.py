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
    #optionData = back1.data_query.get_menu_option()

    #cartList
    def Reset_lcd_Price(self) :
        self.lcd_Price.display(self.totalPrice)

    def cartWidget_Add(self, menuData) :
        optionList = []
        #data = ['테스트 메뉴', optionList, 1, 2000]
        item_Widget = front.cartItem(self.cartList, menuData, self)
        item = QListWidgetItem()
        item.setSizeHint(item_Widget.sizeHint())

        self.cartList.addItem(item)
        self.cartList.setItemWidget(item, item_Widget)
    
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
        self.cartList = self.cart_List

        #test = front.cartItem(self.cartList, self.data, self)
        #test.cartItem_Add(self.data)

        self.set_MainPage_Index(0)
        self.setup_MenuList()

    #need to change def name
    def add_timer(self) :
        self.timer.remain_Time += self.timer.timeout_Time
        self.lcd_Timer.display(self.timer.remain_Time)

    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

#Buttons
    #move to initPage
    def mainPage_toInit(self) :
        try :
            self.timer.timeout_Stop()
            self.set_MainPage_Index(0)
            self.setup_MenuList()
        except : 
            self.set_MainPage_Index(0)
            self.setup_MenuList()

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

    #open checkOrderDialog(결제최종확인)
    def popup_checkOrder(self) :
        if self.totalPrice > 0 :
            self.timer.timeout_Pause()

            checkOrder_Window = front.OrderWindow(self)
            checkOrder_Window.order_Price.display(self.totalPrice)
            checkOrder_Window.showModal()

        else :
            #아무것도 주문하지 않았을 시 알림창
            pass

    #menuList//NEED TO REFACTOR
    def setup_MenuList(self) :
        self.menuIndex = 0
        self.menuType = 'ALL'
        self.load_MenuList(self.menuType)
    
    def load_MenuList(self, menuType) :
        self.reset_MenuList()
        i = 0

        menuData = front.get_db(menuType)

        if self.menuIndex == 0 :
            self.btn_menuPrev.setDisabled(True)
        else :
            self.btn_menuPrev.setEnabled(True)

        if self.menuIndex + 8 < len(menuData) :
            self.btn_menuNext.setEnabled(True)
        else :
            self.btn_menuNext.setDisabled(True)

        for item in menuData[self.menuIndex:self.menuIndex + 8] :
            menuStr = 'self.menuWidget_'+str(i)+'.setMenuItem(item, self)'
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

    #btnMenu//NEED TO REFACTOR

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

######################################################

    def btnTEST(self) :
        testData = back1.data_query.get_menu_option()
        testOptionData = []
        for key, data in testData.items() :
            #testOptionList = data
            testOptionData.append([key, data])
        
        print(testData['디카페인 바닐라라떼'])


######################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()