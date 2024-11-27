import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from front import *
import back1
#import back2

import resources_rc

#UI Loading
Init_Class = uic.loadUiType("front/UI/Init.ui")[0]
conn = back1.create_connection()

class MainWindow(QMainWindow, Init_Class) :
    totalPrice = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.init_setting()

#Initial_Settings(execute once)/초기 설정(한번만 실행됨)
    def init_setting(self) :
        #Timer_Init 
        self.timer = timeoutClass(self)
        self.lcd_Timer.display(180)

        #CartList_Init
        self.cartList = self.cartListWidget

        #MenuList_Init
        self.menuList = self.menuListWidget
        menuWidget_Load(self, 'ALL', conn)

        #aiCartList_Init
        self.aiCartList = self.aiCartListWidget

        self.set_MainPage_Index(0)

    #Timer_AddTime/타이머 시간추가
    def add_timer(self) :
        self.timer.add_timer()
        
    #Reset_PriceLCD/가격표시LCD 새로고침
    def Reset_lcd_Price(self) :
        self.lcd_Price.display(self.totalPrice)
        self.lcd_aiPrice.display(self.totalPrice)

#Move_Page/화면 전환(stackedWidget 관련)
    def set_MainPage_Index(self, index) :
        self.mainPage.setCurrentIndex(index)

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
        btn_CartListClear(self)
        self.aiCartList.clear()

    #move to defaultMenuPage
    def mainPage_toDefault(self) :
        self.lcd_Timer.display(180)
        self.timer.timeout_Start(self.timer.TIMEOUT_TIME)
        self.set_MainPage_Index(2)

    #move to voiceOrderPage
    def mainPage_toVoice(self) :
        self.set_MainPage_Index(3)

        testDialog = aiDialog(self, conn)
        testDialog.showModal()
#Move_Page

#btn_MenuType/메뉴종류 설정('ALL', '디카페인', '커피', '티(음료)', '디저트')
    def btn_MenuALL(self) :
        menuWidget_Load(self, 'ALL', conn)
        
    def btn_MenuCoffee(self) :
        menuWidget_Load(self, '커피', conn)
        
    def btn_MenuDeCaffeine(self) :
        menuWidget_Load(self, '디카페인', conn)
        
    def btn_MenuDrinks(self) :
        menuWidget_Load(self, '티', conn)
        
    def btn_MenuDessert(self) :
        menuWidget_Load(self, '디저트', conn)    
#btn_MenuType

#btn_ETC/기타 버튼
    def btn_CartListClear(self) :
        btn_CartListClear(self)

    def popup_Receipt(self) :
        if self.totalPrice > 0 :
            self.timer.timeout_Pause()

            totalOrderData = []

            row = 0
            while True :
                data = self.cartList.item(row) 
                if data != None :
                    orderData = self.cartList.itemWidget(data).get_CartData()
                    totalOrderData.append(orderData)
                    row += 1
                else :
                    break
 
            print(totalOrderData)
            purchaseWindow = front.purchaseWindow(totalOrderData, self)
            purchaseWindow.order_Price.display(self.totalPrice)
            purchaseWindow.showModal()
#btn_ETC

######################################################

    def btnTEST(self) :
        pass

    def btnTEST2(self) :
        pass

    def btn_newAiOrder(self) :
        testDialog = front.aiDialog(self, conn)
        testDialog.showModal()
    
    def addAiCart(self, data) :
        aiCartWidget_Add(self, data)

    def Close(self) :
        back1.close_connection(conn)
        self.close()

######################################################

if __name__ == "__main__":

    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.showFullScreen()
    app.exec_()