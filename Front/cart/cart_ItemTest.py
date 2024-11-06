from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

#data = ['테스트 메뉴', '옵션 없음', 1, 2000]

form_class = uic.loadUiType("front/cart/cartItem.ui")[0]

class cartItem(QWidget, form_class) :
    listWidget = None
    def __init__(self, listWidget, menuData, optionData, parent) :
        super(cartItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.menuData = menuData
        print(self.parent)
        self.listWidget = listWidget
        
        self.menuName.setText(menuData[0])
        optionList = ''.join(menuData[1])
        self.optionList.setText(optionList)
        self.amount.setText('1')
        self.itemPrice.setText(str(menuData[3]))

        print(self.parent.totalPrice)
        self.parent.totalPrice += menuData[3]

    def cartItemAmount_Increase(self) :
        amount = int(self.amount.text())
        amount += 1
        self.parent.totalPrice += self.menuData[3]

        self.amount.setText(str(amount))
        self.parent.Reset_lcd_Price()

    def cartItemAmount_Decrease(self) :
        amount = int(self.amount.text())
        amount -= 1

        if amount == 0 :
            self.cartItem_Remove()
        else :
            self.parent.totalPrice -= self.menuData[3]

        self.amount.setText(str(amount))
        self.parent.Reset_lcd_Price()

    #def cartItem_Add(self, menuData) :
        #self.parent.testMethod(menuData)
    
    def cartItem_Remove(self) :
        self.parent.totalPrice -= self.menuData[3] * int(self.amount.text())

        item = self.listWidget.itemAt(self.pos())
        row = self.listWidget.row(item)
        self.listWidget.takeItem(row)

    #def cartItem_Reset(self) :
        #self.listWidget.clear()