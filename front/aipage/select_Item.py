from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/aiPage/select_Item.ui")[0]

class cartItem(QWidget, form_class) :
    listWidget = None

    def __init__(self, listWidget, menuData, parent) :
        super(cartItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent
