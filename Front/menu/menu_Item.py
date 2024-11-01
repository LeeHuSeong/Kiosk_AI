from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("Front/menu/menuItem.ui")[0]

class menuItem(QWidget, form_class) :
    def __init__(self, parent = None) :
        super(menuItem, self).__init__(parent)
        self.setupUi(self)

        item = "defaultImage"
        src = QPixmap("./img/"+ item +".jpg").scaled(150, 150)
        self.menuImg.setPixmap(src)

    def setMenuItem(self, imgPath, menuPrice) :
        imgPath = imgPath
        #print(imgPath)
        src = QPixmap(imgPath).scaled(150, 150)
        self.menuImg.setPixmap(src)

        menu = imgPath.split('\\')[2]
        self.menuName.setText(menu)
        self.menuPrice.setText("\\" + str(menuPrice))
    
    def setMenuItemDefault(self) :
        imgPath = "./img/defaultImage.jpg"
        src = QPixmap(imgPath).scaled(150, 150)
        self.menuImg.setPixmap(src)
        menu = imgPath.split('/')[2]
        self.menuName.setText(menu)
        self.menuPrice.setText("\\0")

    def addShoppingCart(self) :
        print("test message")

