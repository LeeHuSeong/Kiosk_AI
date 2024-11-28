from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

import ast

import front
#menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 0, ['AddDeShot', 'AddStevia'], 'desc']
form_class_0 = uic.loadUiType("front/menu/menu_Item.ui")[0]
form_class_1 = uic.loadUiType("front/menu/menu_ItemSet.ui")[0]

class menuItemClass(QWidget, form_class_0) :

    def __init__(self, parent = None) :
        super(menuItemClass, self).__init__(parent)
        self.setupUi(self)

    def menuItem_Init(self, parent, conn, menuData) :
        self.__parent = parent
        self.__conn = conn
        self.__menuData = menuData

        menuNameStr = self.menuData[2].split('\\').replace('.jpg', '').split('_')

        self.__menuName = menuNameStr[1]            # STR
        self.__menuImg = QtGui.QIcon(menuData[2])   # QtGui 객체
        self.__Price = menuData[1]                  # INT
        self.__HotIce = menuNameStr[0]              # STR

        self.set_LabelData()

    #Getter
    @property
    def conn(self) :
        return self.__conn
    @property
    def menuData(self) :
        return self.__menuData
    @property
    def menuName(self) :
        return self.__menuName
    @property
    def menuImg(self) :
        return self.__menuImg
    @property
    def menuPrice(self) :
        return self.__Price
    @property
    def HotIce(self) :
        return self.__HotIce 
    
    def set_LabelData(self) :
        self.menuName_.setText(self.menuName)
        self.menuImg_.setIcon(self.menuImg)
        self.menuImg_.setIconSize(QSize(198, 198))
        self.menuPrice_.setText(self.menuPrice)

        if self.HotIce == 'HOT' :
            self.menuHot_.setText(self.HotIce)
        else :
            self.menuIce_.setText(self.HotIce)


    def open_selectOptionPage(self) :

        self.parent.timer.timeout_Pause()
        
        selectOptionPage = front.optionWindowClass_Default(self.parent, self.conn, self.menuData)
        selectOptionPage.showModal()

        result = selectOptionPage.result
        self.parent.timer.timeout_Resume(self.parent.timer.remain_Time)
        front.cartWidget_Add(self.parent, result)

class menu_ItemSet(QWidget, form_class_1) :

    def __init__(self, parent, conn, listWidget, menuData) :
        super(menu_ItemSet, self).__init__(parent)
        self.setupUi(self)

        self.__parent = parent
        self.__conn = conn
        self.__listWidget = listWidget
        self.__menuData = menuData

        for i in range(1, 5):
            widget_name = f'widget_{i}'
            widget = getattr(self, widget_name)
            if i > len(menuData) :
                break
            else :
                widget.menuItem_Init(self.parent, self.conn, self.menuData)

    #Getter
    @property
    def parent(self) :
        return self.__parent
    @property
    def conn(self) :
        return self.__conn
    @property
    def menuData(self) :
        return self.__menuData

class menuClass :
    pass