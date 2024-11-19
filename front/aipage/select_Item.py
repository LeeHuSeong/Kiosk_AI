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

        self.parent.menuStr.setText(self.menuData[0])   #메뉴이름
        self.parent.menuDesc.setText(self.menuData[1])  #메뉴설명

        pixmap = QPixmap(self.menuData[2]).scaled(300, 300)  #메뉴이미지
        self.parent.menuImg.setPixmap(pixmap)
        self.parent.lcdNumber.display(self.menuData[4])

        self.parent.menuData = [self.menuData[0], self.menuData[1], self.menuData[2], self.menuData[4]]
        self.parent.optionData = self.menuData[3]