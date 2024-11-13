from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

form_class = uic.loadUiType("front/menu/menuItem.ui")[0]

class menuItem(QWidget, form_class) :

    def __init__(self, parent = None) :
        super(menuItem, self).__init__(parent)
        self.setupUi(self)

        #menuName = self.menuData[0]
        #menuPrice = self.menuData[1]
        #menuImgPath = self.menuData[2]

        #btn
        #self.menuImg

        #label
        #self.menuData
        #self.menuName
        #self.menuPrice
    def get_TEST(self) :
        print(self.menuName.text())

    def menuItem_Init(self) :
        menuDataText = self.menuData.text()
        menuData = menuDataText.strip("[]").replace("'", "").split(", ")

        self.menuName.setText(menuData[0])
        self.menuPrice.setText(str(menuData[1]))
        self.menuImg.setIcon(QtGui.QIcon(menuData[2]))
        self.menuImg.setIconSize(QSize(200, 200))
        #print(menuData[0])

    def open_selectOptionPage(self) :
        print(self.menuName.text())
