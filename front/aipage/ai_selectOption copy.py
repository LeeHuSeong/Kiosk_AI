from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import front
import back1

from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("front/aipage/ai_selectOption.ui")[0]
#menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]
class aiOptionWindow(QDialog, form_class) :
    optionDict = {}
    
    menuName = ''           # (STR) 메뉴 이름]
    menuDesc = ''
    menuDefaultPrice = 0    # (INT) 메뉴 기본가격 
    menuImgSrc = ''         # (STR) 메뉴 이미지 주소
    menuAmount = 1          # (INT) 주문 수량
    #menuOption = []         # (LIST[STR]) 선택한 옵션 리스트
    singlePrice = 0         # (INT) 옵션 포함 1개 가격
    totalPrice = 0          # (INT) 옵션 포함 전체 가격

    menuData = []
    optionData = []

    selectedOptionNameDict = {}
    selectedOptionIDDict = {}

    def __init__(self, menuData, parent) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.set_InitData(menuData, parent)
        self.set_InitLabelData()

    # Initial_Setting
    def set_InitData(self, menuData, parent) :  #초기 Class 변수 값 설정
        self.parent = parent

        #버튼변수 할당
        for key in self.optionDict : 
            for value in self.optionDict[key] :
                value.clicked.connect(self.optionSelect)

        self.menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        self.menuDesc = menuData[5]

        self.menuDefaultPrice = menuData[1]
        self.totalPrice = menuData[1]

        self.menuImgSrc = menuData[2]
        self.menuAmount = menuData[3]

        self.optionData = menuData[4]
        self.set_InitSetting(self.optionData)

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
    
    def set_InitLabelData(self) :       #초기 Label 값 설정
        self.menuName_.setText(self.menuName)
        self.menuDesc_.setText(self.menuDesc)

        pixmap = QPixmap(self.menuImgSrc).scaled(150, 150)
        self.menuImg_.setPixmap(pixmap)

        self.itemPrice_.setText(str(self.totalPrice) + '원')

    def set_InitSetting(self, optionData) :
        i = 0
        for key in self.optionDict :
            if key in optionData :
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

    def refresh_Price(self) :
        data = self.selectedOptionIDDict.items()
        optPrice = 0

        if data != {} :
            for key, value in data :
                optPrice += int(back1.get_opt_price(key, value))

        return optPrice

    def selectOption_Cancel(self) :
        #self.parent.timer.timeout_Resume(self.parent.timer.remain_Time)
        self.close()

    def selectOption_Add(self) :
        result = [self.selectedOptionNameDict, 1, self.priceLabel.text().split('원')[0]]

        self.parent.optionResult = result
        self.close()

    def optionSelect(self) :
        sender = self.sender()
        getKey = sender
        getValue = sender.objectName()

        key = self.get_key(getKey)
        value = self.get_value(getValue)

        self.selectedOptionIDDict[key] = int(value)
        self.totalPrice = self.refresh_Price() + self.originPrice
        self.priceLabel.setText(str(self.totalPrice) + '원')

        if key == 'AddShot' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '1샷 추가'
            elif int(value) == 2 :
                self.selectedOptionNameDict[key] = '2샷 추가'

        elif key == 'AddDeShot' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '디카페인 1샷 추가'

        elif key == 'ChangeStevia' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '스테비아 변경'
        
        elif key == 'AddStevia' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '스테비아 추가'
        
        elif key == 'AddVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '바닐라시럽 추가'
        
        elif key == 'ChangeLightVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '라이트 바닐라시럽 변경'
        
        elif key == 'AddLightVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '라이트 바닐라시럽 추가'
        
        elif key == 'AddCaramel' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '카라멜시럽 추가'
        
        elif key == 'SelectMilk' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '우유 변경(아몬드)'
            elif int(value) == 2 :
                self.selectedOptionNameDict[key] = '우유 변경(오트)'
        
        elif key == 'AddHoney' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionNameDict[key] = '꿀 추가'
        
        elif key == 'AddWhipping' :
            if int(value) == 0 :
                self.selectedOptionNameDict[key] = '휘핑 빼기'
            elif int(value) == 1 :
                pass
        
        elif key == 'AddCinnamon' :
            if int(value) == 0 :
                self.selectedOptionNameDict[key] = '시나몬 빼기'
            elif int(value) == 1 :
                pass       

    def get_key(self, val) :
        for key in self.optionDict : 
            for value in self.optionDict[key] :
                if val == value :
                    return key
                
    def get_value(self, objectName) :
        return objectName[-1]