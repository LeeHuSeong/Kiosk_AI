from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap
import time

import front
import back1
import AI.AI_main

form_class = uic.loadUiType("front/aipage/ai_Dialog.ui")[0]

class aiDialog(QDialog, form_class) :
    #Page_0
    resultFlag = 0
    result = []
    parent = None
    conn = 0

    #Page_1
    menuData = []

    #Page_2
    menuName = ''
    menuDesc = ''
    itemPrice = 0
    menuImgSrc = ''
    menuOption = []
    optionResult = [{}, {}, 0]
    optionList = []

    def __init__(self, parent, conn) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.conn = conn
        self.parent = parent
        self.aiOptionList = self.aiOptionListWidget
        self.aiInExactList = self.ai_InExactListWidget
        self.stackedWidget.setCurrentIndex(0)

    def showModal(self) :
        return super().exec_()
    
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btn_Start(self) :
        self.optionResult = [{}, {}, 0] #선택옵션리스트 초기화
        voiceResult = None
        self.result = []        #결과
        self.resultFlag = -1     #결과 종류(0: 정확한 결과, 1: 부정확한 결과(리스트), -1: 입력 오류)
        
        #음성입력 시작

        #여기에 작성 및 result 변수/ resultFlag 변수에 결과 할당
        voiceResult = AI.AI_main.AI_recognition(self.conn)
        #[['아메리카노'], 1, 0, ['아이스 아메리카노']]

        if voiceResult != None :
            self.result = [voiceResult[0], voiceResult[1]]
            self.resultFlag = voiceResult[2]
        else :
            return

        #음성입력 완료 및 결과반환

        #결과가 정확하다면
        if self.resultFlag == 0 :
            self.stackedWidget.setCurrentIndex(2)
            self.menuData = AI.AI_main.get_AI_menu_data(self.conn, self.result[0], self.result[1], self.resultFlag)
            #print(self.menuData)
            self.set_aiOrderData(self.menuData[0])

        #결과가 부정확하다면
        elif self.resultFlag == 1:
            inputStr = voiceResult[3]
            self.InputStr_2.setText('입력 결과: ' + inputStr)
            #result = [['메뉴명1', '메뉴명2', ...], 수량]
            self.result = [['디카페인 아메리카노', '아메리카노', '디카페인 카페라떼'], 1]

            self.stackedWidget.setCurrentIndex(1)
            #메뉴리스트 ListWidget item으로 반환
            for data in self.menuData :
                self.addInExactList(data)            

        #오류
        else :
            pass

    # Initial_Setting
    def set_aiOrderData(self, menuData) :
        #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]

        self.set_InitData(menuData)
        self.set_LabelData()

    def set_InitData(self, menuData) :
        self.menuData = menuData
        self.menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        self.menuDesc = menuData[5]
        self.itemPrice = menuData[1]
        self.menuImgSrc = menuData[2]
        self.menuOption = menuData[4]

    def set_LabelData(self) :
        self.menuName_.setText(self.get_menuName())                 #메뉴이름
        self.menuDesc_.setText(self.get_menuDesc())                 #메뉴설명
        
        pixmap = QPixmap(self.get_menuImgSrc()).scaled(300, 300)
        self.menuImg_.setPixmap(pixmap)                             #메뉴이미지
        
        self.itemPrice_.display(self.get_itemPrice())

    # getter
    def get_menuData(self) :
        return self.menuData
    def get_menuName(self) :            #STR
        return self.menuName
    def get_itemPrice(self) :
        return self.itemPrice
    def get_menuDesc(self) :            #STR
        return self.menuDesc
    def get_menuImgSrc(self) :          #STR
        return self.menuImgSrc
    def get_menuOption(self) :          #LIST[STR]
        return self.menuOption
    def get_optionResult(self) :
        return self.optionResult
    # setter
    def set_menuData(self, menuData) :  #메뉴데이터 설정
        self.menuData = menuData
    def set_optionResult(self, value) :
        self.optionResult = value
        self.itemPrice = value[2]

    # def
    def btn_Back(self) :
        #print(self.resultFlag)
        #print(self.stackedWidget.currentIndex())
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
        self.aiOptionListWidget.clear()
        #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]

        popup_selectOption = front.aiOptionWindow(self, self.menuData, self.optionResult, self.conn)
        popup_selectOption.showModal()

        self.optionList = []
        self.itemPrice_.display(self.get_itemPrice())
        for value in self.optionResult[0].items() :
            self.aiOptionListWidget.addItem(value[1])
            self.optionList.append(value[1])

    def btn_addCart(self) :
        if int(self.optionResult[2]) != 0 :
            data = [self.menuData[0], int(self.optionResult[2]), self.menuData[2], 1, self.optionList, self.result[1]]
            #self.optionResult = [{}, {}, 0]
        else :
            data = [self.menuData[0], self.menuData[1], self.menuData[2], 1, self.optionList, self.result[1]]
            #self.optionResult = [{}, {}, 0]
        #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg']
        #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]
        #
        self.parent.addAiCart(data)
        self.close()

    def addInExactList(self, menuData) :
        item_Widget = front.inExactItem(self.aiInExactList, menuData, self)
        item = QListWidgetItem()
        item.setSizeHint(item_Widget.sizeHint())

        self.aiInExactList.addItem(item)
        self.aiInExactList.setItemWidget(item, item_Widget)
    