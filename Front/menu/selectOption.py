from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

Order_Class = uic.loadUiType("front/menu/selectOption.ui")[0]

class OrderWindow(QDialog, Order_Class) :
    def __init__(self, menuData, optionData, parent) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.parent = parent
        print(optionData[1])
        testOptionData = [0, 1, 6, 4, 5, 9, 8]

        self.selectedOptionDict = {}
        self.optionDict = {
            'AddShot'           : [self.btn_Shot_0, self.btn_Shot_1, self.btn_Shot_2] ,             #0 샷 추가
            'AddDeShot'         : [self.btn_DeShot_0, self.btn_DeShot_1] ,                          #1 디카페인 샷 추가
            'ChangeStevia'      : [self.btn_ChangeStev_0, self.btn_ChangeStev_1] ,                  #2 스태비아 변경
            'AddStevia'         : [self.btn_AddStev_0, self.btn_AddStev_1] ,                        #3 스태비아 추가
            'AddVanila'         : [self.btn_AddVan_0, self.btn_AddVan_1] ,                          #4 바닐라시럽 추가
            'ChangeLightVanila' : [self.btn_ChangeLightVan_0, self.btn_ChangeLightVan_1] ,          #5 라이트 바닐라시럽 변경
            'AddLightVanila'    : [self.btn_AddLightVan_0, self.btn_AddLightVan_1] ,                #6 라이트 바닐라시럽 추가
            'AddCaramel'        : [self.btn_AddCaramel_0, self.btn_AddCaramel_1] ,                  #7 카라멜시럽 추가
            'SelectMilk'        : [self.btn_SelectM_0, self.btn_SelectM_1, self.btn_SelectM_2] ,    #8 우유 선택
            'AddHoney'          : [self.btn_AddHoney_0, self.btn_AddHoney_1] ,                      #9 꿀 추가
            'AddWhipping'       : [self.btn_Whipping_0, self.btn_Whipping_1] ,                      #10 휘핑OX
            'AddCinnamon'       : [self.btn_Cinnamon_0, self.btn_Cinnamon_1]                        #11 시나몬 OX
        }

        for key in self.optionDict : 
            for value in self.optionDict[key] :
                value.clicked.connect(self.optionSelect)

        self.selectOption_InitSetting(optionData)

        self.selectOption_MenuName.setText(menuData[0])
        self.selectOption_Price.setText(str(menuData[1]) + '원')

    def selectOption_InitSetting(self, optionData) :
        i = 0
        for key in self.optionDict :
            if key in optionData[1] :
                initStr = 'self.frame_Option_'+str(i)+'.setVisible(True)'
            else :
                initStr = 'self.frame_Option_'+str(i)+'.setVisible(False)'
            eval(initStr)
            i += 1

    #창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    #창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def selectOption_Cancel(self) :
        self.parent.timer.timeout_Resume(self.parent.timer.remain_Time)
        self.close()

    def selectOption_Add(self) :
        result = {}
        pass

    def optionSelect(self) :
        sender = self.sender()
        getKey = sender
        getValue = sender.objectName()

        key = self.get_key(getKey)
        value = self.get_value(getValue)

        self.selectedOptionDict[key] = value
        print(self.selectedOptionDict)

    def get_key(self, val) :
        for key in self.optionDict : 
            for value in self.optionDict[key] :
                if val == value :
                    return key
                
    def get_value(self, objectName) :
        return objectName[-1]




