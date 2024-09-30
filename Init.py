import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("Init.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.mainPage.setCurrentIndex(0)

#Buttons
    def btn_ToInitPage(self) :
        self.mainPage.setCurrentIndex(0)

    def btn_ToSelectPage(self) :
        self.mainPage.setCurrentIndex(1)

    def btn_ToDefaultMenuPage(self) :
        self.mainPage.setCurrentIndex(2)

    def btn_ToVoiceOrderPage(self) :
        self.mainPage.setCurrentIndex(3)

    def btn_ToOrderPage(self) :
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow()
    myWindow.show()
    app.exec_()