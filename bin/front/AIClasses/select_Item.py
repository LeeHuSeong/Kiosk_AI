from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("bin/front/AIClasses/select_Item.ui")[0]
class inExactItem(QWidget, form_class) :
    listWidget = None
    menuData = []

    menuName = ''           # (STR) 메뉴 이름
    menuDefaultPrice = 0    # (INT) 메뉴 기본가격 

    #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]
    def __init__(self, listWidget, menuData, parent) :
        super(inExactItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.listWidget = listWidget
        self.menuData = menuData

        self.menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        self.menuDefaultPrice = menuData[1]

        self.menuName_.setText(self.menuName)
        self.itemPrice_.setText(str(self.menuDefaultPrice) + '원')

    def btn_select(self) : 
         self.parent.stackedWidget.setCurrentIndex(2)
         self.parent.aiOrderData__init__(self.menuData)