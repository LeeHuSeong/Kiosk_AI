from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("front/aiPage/select_Item.ui")[0]

class inExactItem(QWidget, form_class) :
    listWidget = None
    menuData = []

    def __init__(self, listWidget, menuData, parent) :
        super(inExactItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.listWidget = listWidget
        self.menuData = menuData

        self.menuName_.setText(menuData[0])
        self.itemPrice_.setText(str(menuData[4]) + '원')

    def btn_select(self) : 
        self.parent.stackedWidget.setCurrentIndex(2)

        self.parent.menuName_.setText(self.menuData[0])   #메뉴이름
        self.parent.menuDesc_.setText(self.menuData[1])  #메뉴설명

        pixmap = QPixmap(self.menuData[2]).scaled(300, 300)  #메뉴이미지
        self.parent.menuImg_.setPixmap(pixmap)
        self.parent.itemPrice_.display(self.menuData[4])

        #self.menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]
        self.parent.menuData = [self.menuData[0], self.menuData[4], self.menuData[2], 1, self.menuData[3], self.menuData[1]]