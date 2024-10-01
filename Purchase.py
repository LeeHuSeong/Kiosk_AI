import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

Purchase_Class= uic.loadUiType("Purchase.ui")[0]

class PurchaseWindow(QMainWindow, Purchase_Class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.center()
        self.show()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def window_Close(self) :
        self.close()

    def purchasePage_Submit(self) :
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = PurchaseWindow()
    myWindow.show()
    app.exec_()