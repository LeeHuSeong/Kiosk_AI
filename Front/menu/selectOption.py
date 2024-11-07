from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

Order_Class = uic.loadUiType("front/menu/selectOption.ui")[0]
#testOptionData = [0, 1, 2]

class OrderWindow(QDialog, Order_Class) :
    def __init__(self, menuData, optionData) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        testOptionData = [0, 1, 2]
        self.selectOption_InitSetting(testOptionData)
        #self.parent_mainWindow = parent
        self.selectOption_MenuName.setText(menuData[0])
        #if menuData[3] == '디카페인' :


        try :
            print(menuData)
        except :
            pass
        try :
            print(optionData)
        except :
            pass

    def selectOption_InitSetting(self, optionData) :
        for item in range(0, 11) :
            if item in optionData :
                initStr = 'self.frame_Option_'+str(item)+'.setVisible(True)'
            else :
                initStr = 'self.frame_Option_'+str(item)+'.setVisible(False)'

            eval(initStr)
        


    #창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    #창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())