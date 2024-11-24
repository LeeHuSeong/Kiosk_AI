from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

import front
import back1

from PyQt5.QtGui import QPixmap

form_class = uic.loadUiType("front/aipage/ai_selectOption.ui")[0]
#menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]

class aiOptionWindow(QDialog, form_class) :
    # Variables
    optionDict = {}         # (Dict) 버튼 변수 딕셔너리(Init 시 할당)
    menuData = []           # (List) [메뉴이름, 메뉴 기본가격, 메뉴 이미지 주소, 주문 수량, 옵션 목록, 메뉴 설명]
    optionData = []         # (List) [menuData[4]]/선택 가능한 옵션 목록 ex(['AddDeShot', 'AddVanila'])
    optionResult = []       # (List) 이전 선택 결과/기본값 [{}, {}, 0]
    conn = None

    menuName = ''           # (STR) 메뉴 이름
    menuDesc = ''           # (STR) 메뉴 설명
    menuDefaultPrice = 0    # (INT) 메뉴 기본가격 
    menuImgSrc = ''         # (STR) 메뉴 이미지 주소
    menuAmount = 1          # (INT) 주문 수량
    optionPrice = 0         # (INT) 총 선택옵션 가격
    totalPrice = 0          # (INT) 메뉴+옵션 가격/menuDefaultPrice + optionPrice

    selectedOptionName = {} # (Dict) 결과 출력용 선택옵션 딕셔너리
    selectedOptionID = {}   # (Dict) 내부 연산용 선택옵션 딕셔너리

    # __init__
    def __init__(self, parent, menuData, optionResult, conn) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.set_InitData(parent, menuData, optionResult, conn)
        self.set_LabelData()

    #getter
    def get_totalPrice(self) :
        return self.totalPrice
    #setter
    def set_totalPrice(self, val) :
        self.totalPrice = val

    # 초기 변수 설정(객체 생성 시 1번 실행)
    def set_InitData(self, parent, menuData, optionResult, conn) :
        self.parent = parent
        self.menuData = menuData
        self.optionData = menuData[4]
        self.optionResult = optionResult
        self.conn = conn

        self.menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        self.menuDesc = menuData[5]
        self.menuDefaultPrice = menuData[1]
        self.menuImgSrc = menuData[2]
        self.menuAmount = menuData[3]

        self.selectedOptionName = optionResult[0]
        self.selectedOptionID = optionResult[1]

        # 이전 선택 결과 로딩
        if optionResult[2] == 0 :   # 옵션 선택 X or 옵션 선택창 클릭 X
            self.totalPrice = self.menuDefaultPrice
        else :
            self.totalPrice = optionResult[2]

        # 버튼 변수 할당
        self.optionDict = {
            'Addshot'           : [self.btn_Shot_0, self.btn_Shot_1, self.btn_Shot_2] ,             #0 샷 추가
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
    
        # 버튼 이벤트 연결/이전 선택내용이 있다면 이전 선택결과 출력
        for key in self.optionDict :
            i = 0
            for value in self.optionDict[key] :
                value.clicked.connect(self.optionSelect)
                if key in optionResult[1] and i == optionResult[1][key] :
                    value.setChecked(True)
                i += 1

        # 필요없는 옵션항목 숨기기
        i = 0
        for key in self.optionDict :
            if key in self.optionData :
                defStr = 'self.frame_Option_' + str(i) + '.setVisible(True)'
            else :
                defStr = 'self.frame_Option_' + str(i) + '.setVisible(False)'
            eval(defStr) # 실행
            i += 1
    
    # Label Text, Pixmap 설정
    def set_LabelData(self) :
        self.menuName_.setText(self.menuName)
        self.menuDesc_.setText(self.menuDesc)

        pixmap = QPixmap(self.menuImgSrc).scaled(150, 150)
        self.menuImg_.setPixmap(pixmap)
        self.itemPrice_.setText(str(self.totalPrice) + '원')

    # 옵션버튼 클릭 시 가격 변경
    def refresh_Price(self) :
        data = self.selectedOptionID.items()
        optionPrice = 0

        if data != {} :
            for key, value in data :
                optionPrice += int(back1.get_opt_price(self.conn, key, value))
        
        return optionPrice
    # 옵션 버튼 클릭 이벤트 ###############
    def optionSelect(self) :
        sender = self.sender()
        getKey = sender
        getValue = sender.objectName()

        key = self.get_key(getKey)
        value = self.get_value(getValue)

        self.selectedOptionID[key] = int(value)
        self.set_totalPrice(self.refresh_Price() + self.menuDefaultPrice)
        self.itemPrice_.setText(str(self.get_totalPrice()) + '원')

        self.set_selectedOptionName(key, value)
        
    def set_selectedOptionName(self, key, value) :
        if key == 'Addshot' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '1샷 추가'
            elif int(value) == 2 :
                self.selectedOptionName[key] = '2샷 추가'

        elif key == 'AddDeShot' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '디카페인 1샷 추가'

        elif key == 'ChangeStevia' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '스테비아 변경'
        
        elif key == 'AddStevia' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '스테비아 추가'
        
        elif key == 'AddVanila' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '바닐라시럽 추가'
        
        elif key == 'ChangeLightVanila' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '라이트 바닐라시럽 변경'
        
        elif key == 'AddLightVanila' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '라이트 바닐라시럽 추가'
        
        elif key == 'AddCaramel' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '카라멜시럽 추가'
        
        elif key == 'SelectMilk' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '우유 변경(아몬드)'
            elif int(value) == 2 :
                self.selectedOptionName[key] = '우유 변경(오트)'
        
        elif key == 'AddHoney' :
            if int(value) == 0 :
                self.selectedOptionName.pop(key, None)
            elif int(value) == 1 :
                self.selectedOptionName[key] = '꿀 추가'
        
        elif key == 'AddWhipping' :
            if int(value) == 0 :
                self.selectedOptionName[key] = '휘핑 빼기'
            elif int(value) == 1 :
                self.selectedOptionName.pop(key, None)
        
        elif key == 'AddCinnamon' :
            if int(value) == 0 :
                self.selectedOptionName[key] = '시나몬 빼기'
            elif int(value) == 1 :
                self.selectedOptionName.pop(key, None)    
    def get_key(self, val) :
        for key in self.optionDict : 
            for value in self.optionDict[key] :
                if val == value :
                    return key      
    def get_value(self, objectName) :
        return objectName[-1]
    ######################################

    # 버튼 메서드
    def selectOption_Cancel(self) : # 선택 취소
        result = self.optionResult

        self.parent.set_optionResult(result)    # ai_Dialog 객체로 전달
        self.close()

    def selectOption_OK(self) :     # 선택 확인
        result = [self.selectedOptionName, self.selectedOptionID, self.get_totalPrice()]
        
        self.parent.set_optionResult(result)    # ai_Dialog 객체로 전달
        self.close()

    # 창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    # 창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())