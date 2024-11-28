from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .cartItemClass import cartItemClass

class cartClass :
    def cartWidget_Add(self, menuData) :
        item_Widget = cartItemClass(self, self.cartList, menuData)
        item = QListWidgetItem()
        item.setSizeHint(item_Widget.sizeHint())

        self.cartList.addItem(item)
        self.cartList.setItemWidget(item, item_Widget)
        self.Reset_lcd_Price()
    
    def btn_CartListClear(self) :
        self.cartList.clear()
        self.totalPrice = 0
        self.lcd_Price.display(self.totalPrice)