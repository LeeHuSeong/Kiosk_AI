from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

import ast
from front.menu import menu_SelectOption

form_class = uic.loadUiType("front/menu/menu_Item.ui")[0]

class menu_Item(QWidget, form_class) :
    menuData = []
    optionData = []

    def __init__(self, parent = None) :
        super(menu_Item, self).__init__(parent)
        self.setupUi(self)

    def menuItem_Init(self) :
        menuDataText = self.menuData.text()
        self.menuData = ast.literal_eval(menuDataText)
        self.optionData = self.menuData[5]

        #self.menuName.setText(self.menuData[0])
        self.menuName.setText(self.menuData[2].split('\\')[2].replace('.jpg', ''))
                              
        self.menuPrice.setText(str(self.menuData[1]) + '원')

        self.menuImg.setIcon(QtGui.QIcon(self.menuData[2]))
        self.menuImg.setIconSize(QSize(200, 200))

    def set_Parent(self, parent) :
        self.parent = parent

    def open_selectOptionPage(self) :
        self.parent.timer.timeout_Pause()

        selectOptionPage = menu_SelectOption.optionWindow(self.menuData, self.optionData, self.parent)
        selectOptionPage.showModal()
