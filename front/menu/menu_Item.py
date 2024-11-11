from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

from front.menu import selectOption

form_class = uic.loadUiType("front/menu/menuItem.ui")[0]

class menuItem(QWidget, form_class) :
    def __init__(self, parent = None) :
        #parent, menuData, optionData
        super(menuItem, self).__init__(parent)
        self.setupUi(self)

        self.menuImg.setIcon(QtGui.QIcon("./img/defaultImage.jpg"))
        self.menuImg.setIconSize(QSize(200, 200))

    def setMenuItem(self, menuData, parent) :
        self.parent = parent
        self.menuData = menuData
        self.menuImg.setIcon(QtGui.QIcon(menuData[2]))
        self.menuImg.setIconSize(QSize(200, 200))
        menu1 = menuData[2].split('\\')[2]
        menu = menu1.split('.')[0]
        self.menuName.setText(menu)
        self.menuPrice.setText("\\" + str(menuData[1]))
    
    def setMenuItemDefault(self) :
        imgPath = "./img/defaultImage.jpg"

        self.menuImg.setIcon(QtGui.QIcon(imgPath))
        self.menuImg.setIconSize(QSize(200, 200))
        menu = imgPath.split('/')[2]
        self.menuName.setText(menu)
        self.menuPrice.setText("\\0")

    def select_MenuOption(self) :
        #optionList = selectOption.OrderWindow()
        self.parent.timer.timeout_Pause()
        self.optionData = []
        try :
            self.optionData = self.parent.optionData[self.menuData[0]]
        except :
            pass

        test = selectOption.OrderWindow(self.menuData, self.optionData, self.parent)
        test.showModal()
    
    def addShoppingCart(self) :
        optionList = []
        menuPrice = int(self.menuPrice.text().split('\\')[1])
        menuData = [self.menuName.text(), optionList, 1, menuPrice]
        
        self.parent.cartWidget_Add(menuData)
        self.parent.Reset_lcd_Price()
