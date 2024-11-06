from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

form_class = uic.loadUiType("front/menu/menuItem.ui")[0]

class menuItem(QWidget, form_class) :
    def __init__(self, parent = None) :
        super(menuItem, self).__init__(parent)
        self.setupUi(self)

        self.menuImg.setIcon(QtGui.QIcon("./img/defaultImage.jpg"))
        self.menuImg.setIconSize(QSize(200, 200))

    def setMenuItem(self, imgPath, menuPrice, parent) :
        self.parent = parent
        self.menuImg.setIcon(QtGui.QIcon(imgPath))
        self.menuImg.setIconSize(QSize(200, 200))
        menu = imgPath.split('\\')[2]
        self.menuName.setText(menu)
        self.menuPrice.setText("\\" + str(menuPrice))
    
    def setMenuItemDefault(self) :
        imgPath = "./img/defaultImage.jpg"

        self.menuImg.setIcon(QtGui.QIcon(imgPath))
        self.menuImg.setIconSize(QSize(200, 200))
        menu = imgPath.split('/')[2]
        self.menuName.setText(menu)
        self.menuPrice.setText("\\0")

    def addShoppingCart(self) :
        optionList = []
        menuPrice = int(self.menuPrice.text().split('\\')[1])
        menuData = [self.menuName.text(), optionList, 1, menuPrice]
        
        self.parent.cartWidget_Add(menuData)
        self.parent.Reset_lcd_Price()
    

