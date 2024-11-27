from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/cart/cart_Item.ui")[0]

class cartItem(QWidget, form_class) :
    listWidget = None
    menuData = []
    optionList = []

    menuName = ''
    selectedOptionList = ''
    amount = 0
    singleMenuPrice = 0
    totalMenuPrice = 0

    def __init__(self, listWidget, menuData, parent) :
        super(cartItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.menuData = menuData
        self.listWidget = listWidget
        
        self.menuName = menuData[0]
        
        optionList = []
        for value in menuData[1].values() :
            optionList.append(value)
        self.optionList = optionList

        self.selectedOptionList = '\n'.join(self.optionList)
        
        self.amount = menuData[2]
        self.singleMenuPrice = menuData[3]
        self.totalMenuPrice = menuData[3]

        self.menuName_.setText(menuData[0])
        self.optionList_.setText(self.selectedOptionList)
        self.quantity.setText(str(menuData[2]))
        self.itemPrice.setText(str(self.singleMenuPrice) + '원')

        self.btn_cartAmountDec.setDisabled(True)

        self.parent.totalPrice += self.singleMenuPrice

    def cartItemAmount_Increase(self) :
        self.amount += 1

        if self.amount == 1 :
            self.btn_cartAmountDec.setDisabled(True)
        else :
            self.btn_cartAmountDec.setEnabled(True)
            
        self.quantity.setText(str(self.amount))
        self.parent.totalPrice += self.singleMenuPrice

        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()

    def cartItemAmount_Decrease(self) :
        self.amount -= 1

        if self.amount == 1 :
            self.btn_cartAmountDec.setDisabled(True)
        else :
            self.btn_cartAmountDec.setEnabled(True)

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