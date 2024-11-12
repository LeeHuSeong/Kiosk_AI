from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import front
import back1

from PyQt5.QtGui import QPixmap

Order_Class = uic.loadUiType("front/menu/selectOption.ui")[0]

class OrderWindow(QDialog, Order_Class) :
    def __init__(self, menuData, optionData, parent) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.parent = parent

        #testOptionData = [0, 1, 6, 4, 5, 9, 8]
        #self.optPrice = back1.get_opt_price()
        #print(self.optPrice)
        self.selectedOptionDict = {}
        self.selectedOptionDict2 = {}
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

        self.menuName.setText(menuData[0])

        self.originPrice = menuData[1]
        self.totalPrice = menuData[1]
        self.priceLabel.setText(str(self.totalPrice) + '원')

        pixmap = QPixmap(menuData[2]).scaled(150, 150)
        self.menuPic.setPixmap(pixmap)

        desc = back1.get_menu_info(menuData[0])
        self.menuDescription.setText(desc[0])

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
        result = [self.menuName.text(), self.selectedOptionDict, 1, self.priceLabel.text()]
        #print(result)
        self.parent.cartWidget_Add(result)

        self.parent.timer.timeout_Resume(self.parent.timer.remain_Time)
        self.close()

    def optionSelect(self) :
        sender = self.sender()
        getKey = sender
        getValue = sender.objectName()

        key = self.get_key(getKey)
        value = self.get_value(getValue)

        self.selectedOptionDict2[key] = int(value)
        self.totalPrice = self.refresh_Price() + self.originPrice
        self.priceLabel.setText(str(self.totalPrice) + '원')

        if key == 'AddShot' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '1샷 추가'
            elif int(value) == 2 :
                self.selectedOptionDict[key] = '2샷 추가'

        elif key == 'AddDeShot' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '디카페인 1샷 추가'

        elif key == 'ChangeStevia' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '스테비아 변경'
        
        elif key == 'AddStevia' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '스테비아 추가'
        
        elif key == 'AddVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '바닐라시럽 추가'
        
        elif key == 'ChangeLightVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '라이트 바닐라시럽 변경'
        
        elif key == 'AddLightVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '라이트 바닐라시럽 추가'
        
        elif key == 'AddCaramel' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '카라멜시럽 추가'
        
        elif key == 'SelectMilk' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '우유 변경(아몬드)'
            elif int(value) == 2 :
                self.selectedOptionDict[key] = '우유 변경(오트)'
        
        elif key == 'AddHoney' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '꿀 추가'
        
        elif key == 'AddWhipping' :
            if int(value) == 0 :
                self.selectedOptionDict[key] = '휘핑 빼기'
            elif int(value) == 1 :
                pass
        
        elif key == 'AddCinnamon' :
            if int(value) == 0 :
                self.selectedOptionDict[key] = '시나몬 빼기'
            elif int(value) == 1 :
                pass

        #print(self.selectedOptionDict.items())
        


    def get_key(self, val) :
        for key in self.optionDict : 
            for value in self.optionDict[key] :
                if val == value :
                    return key
                
    def get_value(self, objectName) :
        return objectName[-1]

    def refresh_Price(self) :
        data = self.selectedOptionDict2.items()
        optPrice = 0

        if data != {} :
            for key, value in data :
                optPrice += back1.get_opt_price(key, value)

        return optPrice




