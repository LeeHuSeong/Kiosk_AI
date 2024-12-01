from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap
import time

import bin.front
import bin.AI.AI_main

form_class = uic.loadUiType("bin/front/AIClasses/aiDialog.ui")[0]
class aiDialog(QDialog, form_class) :
    def __init__(self, parent, conn) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        # Var_objectData
        self.__parent = parent  
        self.__conn = conn                  # SQL 연결 정보
        self.__menuData = []                # (List) 메뉴 전체 데이터
        self.__optionData = []              # (List) 메뉴 옵션 목록

        # Var_menuData          
        self.__menuName = ''                # (STR) 메뉴 이름
        self.__menuDesc = ''                # (STR) 메뉴 설명
        self.__menuPrice = 0                # (INT) 메뉴 기본 가격
        self.__menuAmount = 0               # (INT) 메뉴 주문 수량
        self.__menuImgSrc = ''              # (STR) 메뉴 이미지 경로

        # Var_listWidget
        self.__aiOptionList = self.aiOptionListWidget       # (listWidget) 옵션 목록 리스트위젯 객체
        self.__aiInExactList = self.ai_InExactListWidget    # (listWidget) 유사메뉴 목록 리스트위젯 객체

        # Var_resultData
        self.__result = []                  # (List) 음성인식 결과 리스트
        self.__resultFlag = 0               # (INT) 결과 종류 (-1: 오류. 0: 해당 메뉴, 1: 유사어 메뉴)
        self.__optionResult = [{}, {}, 0]   # (List) 옵션 선택 결과 반환
        self.__optionList = []              # (List) 옵션 선택 결과 출력 문자열

        self.stackedWidget.setCurrentIndex(0)
        #self.btn_start.setChecked(False)

    # Getter
    @property
    def parent(self) :
        return self.__parent
    @property
    def conn(self) :
        return self.__conn
    @property
    def menuData(self) :
        return self.__menuData
    @property
    def optionData(self) :
        return self.__optionData
    @property
    def menuName(self) :
        return self.__menuName
    @property
    def menuDesc(self) :
        return self.__menuDesc
    @property
    def menuImgSrc(self) :
        return self.__menuImgSrc
    @property
    def menuPrice(self) :
        return self.__menuPrice
    @property
    def menuAmount(self) :
        return self.__menuAmount
    @property
    def aiOptionList(self) :
        return self.__aiOptionList
    @property
    def aiInExactList(self) :
        return self.__aiInExactList
    @property
    def result(self) :
        return self.__result
    @property
    def resultFlag(self) :
        return self.__resultFlag
    @property
    def optionResult(self) :
        return self.__optionResult
    @property
    def optionList(self) :
        return self.__optionList

    # Setter
    @menuData.setter
    def menuData(self, val) :
        self.__menuData = val
    @menuAmount.setter
    def menuAmount(self, val) :
        self.__menuAmount = val
    @optionResult.setter
    def optionResult(self, val) :
        self.__optionResult = val
        self.__menuPrice = val[2]
    @optionList.setter
    def optionList(self, val) :
        self.__optionList = val
    @result.setter
    def result(self, val) :
        self.__result = val
    @resultFlag.setter
    def resultFlag(self, val) :
        self.__resultFlag = val


    # Methods
    def showModal(self) :
        return super().exec_()
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn_Start(self) :
        # 변수 초기화
        self.optionResult = [{}, {}, 0]
        self.result = []        
        self.resultFlag = -1 

        #음성입력 시작
        voiceResult = None
        try :
            voiceResult = bin.AI.AI_main.AI_recognition(self.conn)
        except Exception as e :
            print(f"음성 인식을 시작하지 못했습니다.\n{e}")
            self.resultFlag = -1

        #[['아메리카노'], 1, 0, ['아이스 아메리카노']]

        if voiceResult != None :
            self.result = [voiceResult[0], voiceResult[1]]
            self.resultFlag = voiceResult[2]
        else :
            print("결과를 반환하지 못했습니다.")
            self.btn_start.setChecked(False)
            return
        #음성입력 완료 및 결과반환

        #결과가 정확하다면
        if self.resultFlag == 0 :
            self.menuData = bin.AI.AI_main.get_AI_menu_data(self.conn, self.result[0][0], self.result[1])
            #print(f"self.menuData: {self.menuData}")

            self.aiOrderData__init__(self.menuData)

            self.stackedWidget.setCurrentIndex(2)
            self.btn_start.setChecked(False)

        #결과가 부정확하다면
        elif self.resultFlag == 1 :
            inputStr = str(voiceResult[3])
            self.inputStr_.setText(f"입력 결과: {inputStr}")

            resultList = voiceResult[0]
            #print(f"resultList: {resultList}")

            # aiInExactList에 추가
            for menuName in resultList :
                data = bin.AI.AI_main.get_AI_menu_data(self.conn, menuName, self.result[1])
                self.addInExactList(data)       
            
            self.stackedWidget.setCurrentIndex(1)     
            self.btn_start.setChecked(False)

        #오류
        else :
            self.btn_start.setChecked(False)

    def aiOrderData__init__(self, menuData) :
        #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION']
        print(menuData)
        self.__menuData = menuData
        self.__menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        self.__menuDesc = menuData[5]
        self.__menuPrice = menuData[1]
        self.__menuImgSrc = menuData[2]
        self.__optionData = menuData[4]
        self.__menuAmount = menuData[3]

        self.set_LabelData()

    def set_LabelData(self) :
        self.menuName_.setText(self.menuName)                 #메뉴이름
        self.menuDesc_.setText(self.menuDesc)                 #메뉴설명
        
        pixmap = QPixmap(self.menuImgSrc).scaled(300, 300)
        self.menuImg_.setPixmap(pixmap)                             #메뉴이미지
        
        self.menuAmount_.setText(str(self.menuAmount))
        if self.menuAmount == 1 :
            self.btnDec.setDisabled(True)
        else :
            self.btnDec.setEnabled(True)
        
        self.menuPrice_.display(self.menuPrice)

    def btn_Back(self) :
        if self.stackedWidget.currentIndex() == 1 :
            self.stackedWidget.setCurrentIndex(0)
            self.aiInExactList.clear()
            self.aiOptionList.clear()
        else :
            if self.resultFlag == 0 :
                self.stackedWidget.setCurrentIndex(0)
                self.aiOptionList.clear()
            else :
                self.stackedWidget.setCurrentIndex(1)
                self.aiOptionList.clear()

    def btn_SelectOption(self) :
        self.aiOptionList.clear()
        popup_selectOption = bin.front.optionWindowClass_Voice(self, self.conn, self.menuData, self.optionResult)
        popup_selectOption.showModal()

        self.optionList = []
        self.menuPrice_.display(self.menuPrice)
        for value in self.optionResult[0].items() :
            self.aiOptionList.addItem(value[1])
            self.optionList.append(value[1])

    def btn_addCart(self) :
        #self.optionResult = [{}, {}, 0]
        if int(self.optionResult[2]) != 0 :
            data = [self.menuData[0], int(self.optionResult[2]), self.menuData[2], self.menuAmount, self.optionList, self.result[1]]
        else :
            data = [self.menuData[0], self.menuData[1], self.menuData[2], self.menuAmount, self.optionList, self.result[1]]

        self.parent.addAiCart(data)
        self.close()

    def addInExactList(self, menuData) :
        item_Widget = bin.front.inExactItem(self.aiInExactList, menuData, self)
        item = QListWidgetItem()
        item.setSizeHint(item_Widget.sizeHint())

        self.aiInExactList.addItem(item)
        self.aiInExactList.setItemWidget(item, item_Widget)
    
    def Close(self) :
        print(self.parent.aiCartList.count())
        if self.parent.aiCartList.count() == 0 :
            self.parent.mainPage_toInit()
            self.close()
        else :
            self.close()

    ################################

    def DecreaseAmount(self) :
        currAmount = self.menuAmount - 1
        if currAmount == 1 :
            self.btnDec.setDisabled(True)
        else :
            self.btnDec.setEnabled(True)
        
        self.menuAmount = currAmount
        self.menuAmount_.setText(str(self.menuAmount))

    def IncreaseAmount(self) :
        currAmount = self.menuAmount + 1
        if currAmount != 1 :
            self.btnDec.setEnabled(True)
        
        self.menuAmount = currAmount
        self.menuAmount_.setText(str(self.menuAmount))