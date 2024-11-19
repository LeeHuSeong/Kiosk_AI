from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("front/aipage/test_item.ui")[0]

class aiCartItem(QWidget, form_class) :
    listWidget = None
    menuData = []
    optionList = []

    menuName = ''
    selectedOptionList = ''
    amount = 1
    singleMenuPrice = 0
    totalMenuPrice = 0

    def __init__(self, listWidget, menuData, parent) :
        super(aiCartItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.listWidget = listWidget
        self.optionList = menuData[4]
        
        #self.menuName = menuData[0]
        self.menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        #self.amount = 1
        self.singleMenuPrice = menuData[1]
        self.totalMenuPrice = menuData[1]
        self.parent.totalPrice += self.singleMenuPrice

        pixmap = QPixmap(menuData[2]).scaled(150, 150)
        self.menuPic_.setPixmap(pixmap)

        self.menuName_.setText(self.menuName)
        self.quantity_.setText(str(self.amount))
        self.itemPrice_.setText(str(self.totalMenuPrice) + '원')

        self.selectedOptionList = '\n'.join(self.optionList)
        self.optionList_.setText(self.selectedOptionList)

        self.parent.Reset_lcd_Price()

    def cartItemAmount_Increase(self) :
        self.amount += 1
        self.quantity_.setText(str(self.amount))
        self.parent.totalPrice += self.singleMenuPrice

        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice_.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()

    def cartItemAmount_Decrease(self) :
        self.amount -= 1
        self.quantity_.setText(str(self.amount))

        if self.amount == 0 :
            self.parent.totalPrice -= self.singleMenuPrice
            self.cartItem_Remove()
        else :
            self.parent.totalPrice -= self.singleMenuPrice

        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice_.setText(str(self.totalMenuPrice) + '원')
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
