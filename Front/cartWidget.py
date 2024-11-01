from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("Front/UI/cartWidget.ui")[0]

class cartWidget(QWidget, form_class) :
    def __init__(self, parent = None) :
        super(cartWidget, self).__init__(parent)
        self.setupUi(self)

    def addShoppingCart(self) :
        print("test message")


