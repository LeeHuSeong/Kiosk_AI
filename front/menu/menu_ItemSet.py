from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/menu/menu_ItemSet.ui")[0]

class menu_ItemSet(QWidget, form_class) :
    listWidget = None
    menuData = []
    conn = None

    def __init__(self, listWidget, menuData, parent, conn) :
        super(menu_ItemSet, self).__init__(parent)
        self.setupUi(self)

        self.conn = conn
        self.listWidget = listWidget
        self.menuData = menuData
        self.parent = parent
        print(menuData)

        for i in range(1, 5):
            widget_name = f'widget_{i}'
            widget = getattr(self, widget_name)
            if i > len(menuData) :
                break
            else :
                widget.menuData_.setText(str(menuData[i-1]))
                widget.menuItem_Init(self.conn)
                widget.set_Parent(parent)