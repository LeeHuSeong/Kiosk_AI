from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/cart/menuList_Item.ui")[0]

class menuItem(QWidget, form_class) :
    listWidget = None
    menuData = []

    def __init__(self, listWidget, menuData, parent) :
        super(menuItem, self).__init__(parent)
        self.setupUi(self)

        self.listWidget = listWidget
        self.menuData = menuData
        self.parent = parent
        
        self.menuName = menuData[0]
        
        optionList = []
        for value in menuData[1].values() :
            optionList.append(value)
        self.optionList = optionList

        self.selectedOptionList = '\n'.join(self.optionList)
        
        self.amount = menuData[2]
        self.singleMenuPrice = int(menuData[3].replace('원', ''))
        self.totalMenuPrice = int(menuData[3].replace('원', ''))

        self.menuName_.setText(menuData[0])
        self.optionList_.setText(self.selectedOptionList)
        self.quantity.setText(str(menuData[2]))
        self.itemPrice.setText(str(self.singleMenuPrice) + '원')

        self.parent.totalPrice += self.singleMenuPrice

    def cartItemAmount_Increase(self) :
        self.amount += 1
        self.quantity.setText(str(self.amount))
        self.parent.totalPrice += self.singleMenuPrice

        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()

    def cartItemAmount_Decrease(self) :
        self.amount -= 1
        self.quantity.setText(str(self.amount))

        if self.amount == 0 :
            self.parent.totalPrice -= self.singleMenuPrice
            self.cartItem_Remove()
        else :
            self.parent.totalPrice -= self.singleMenuPrice

        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()
    
    def cartItem_Remove(self) :
        if self.amount == 1 :
            self.parent.totalPrice -= self.singleMenuPrice
            self.amount = 0
        else :
            print(self.singleMenuPrice * self.amount)
            self.parent.totalPrice -= self.singleMenuPrice * self.amount
            self.amount = 0

        self.parent.Reset_lcd_Price()
        item = self.listWidget.itemAt(self.pos())
        row = self.listWidget.row(item)
        self.listWidget.takeItem(row)

    def get_CartData(self) :
        data = [self.menuName, self.optionList, self.amount, self.totalMenuPrice]
        return data