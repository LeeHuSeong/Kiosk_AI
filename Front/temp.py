from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui   


def addShoppingCart(self) :
    optionList = []
    menuPrice = int(self.menuPrice.text().split('\\')[1])
    menuData = [self.menuName.text(), optionList, 1, menuPrice]
        
    self.parent.cartWidget_Add(menuData)
    self.parent.Reset_lcd_Price()
    