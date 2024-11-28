from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from .menuItemClass import menuItemClass

#menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 0, ['AddDeShot', 'AddStevia'], 'desc']
form_class = uic.loadUiType("front/Classes/menuItemSetClass.ui")[0]

class menuItemSetClass(QWidget, form_class) :

    def __init__(self, parent, conn, listWidget, menuData) :
        super(menuItemSetClass, self).__init__(parent)
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
                widget.menuItem_Init(self.parent, self.conn, self.menuData[i-1])

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