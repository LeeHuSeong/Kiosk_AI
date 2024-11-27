from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

import ast

import front

form_class = uic.loadUiType("front/menu/menu_Item.ui")[0]

class menu_Item(QWidget, form_class) :
    menuData = []
    optionData = []
    conn = None

    def __init__(self, parent = None) :
        super(menu_Item, self).__init__(parent)
        self.setupUi(self)

    def menuItem_Init(self, conn) :
        self.conn = conn
        menuDataText = self.menuData.text()
        self.menuData = ast.literal_eval(menuDataText)
        self.optionData = self.menuData[4]

        #self.menuName.setText(self.menuData[0])
        menuStr = self.menuData[2].split('\\')[2].replace('.jpg', '').split('_')
        
        if len(menuStr) == 1 :
            self.menuName.setText(menuStr[0])
        else :
            if menuStr[0] == 'HOT' :
                self.menuHot.setText(menuStr[0])
            else :
                self.menuIce.setText(menuStr[0])

            self.menuName.setText(menuStr[1])
                              
        self.menuPrice.setText(str(self.menuData[1]) + '원')

        self.menuImg.setIcon(QtGui.QIcon(self.menuData[2]))
        self.menuImg.setIconSize(QSize(198, 198))

    def set_Parent(self, parent) :
        self.parent = parent

    def open_selectOptionPage(self) :
        try :
            self.parent.timer.timeout_Pause()
        except :
            pass
        
        selectOptionPage = front.optionWindowClass_Default(self.parent, self.conn, self.menuData)
        selectOptionPage.showModal()