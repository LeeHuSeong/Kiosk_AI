import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

##test
from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("Front/UI/menuItem.ui")[0]

class menuItem(QWidget, form_class) :
    def __init__(self, parent = None) :
        super(menuItem, self).__init__(parent)
        self.setupUi(self)

        item = "defaultImage"
        src = QPixmap("./img/"+ item +".jpg").scaled(200, 200)
        self.menuImg.setPixmap(src)

    def setMenuItem(self, item) :
        menuName = item
        src = QPixmap("./img/"+ menuName +".jpg").scaled(200, 200)
        self.menuImg.setPixmap(src)

        mN = menuName.split('/')[1]

        self.menuName.setText(mN)

    def addShoppingCart(self) :
        print("test message")
