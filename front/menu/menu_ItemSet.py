from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/UI/menuList_Item.ui")[0]

class menu_ItemSet(QWidget, form_class) :
    listWidget = None
    menuData = []

    def __init__(self, listWidget, menuData, parent) :
        super(menu_ItemSet, self).__init__(parent)
        self.setupUi(self)

        #print("log_3" + str(parent))

        self.listWidget = listWidget
        self.menuData = menuData
        self.parent = parent

        for i in range(1, 5):
            widget_name = f'widget_{i}'
            widget = getattr(self, widget_name)
            if i > len(menuData) :
                break
            else :
                widget.menuData.setText(str(menuData[i-1]))
                widget.menuItem_Init()
                widget.set_Parent(parent)