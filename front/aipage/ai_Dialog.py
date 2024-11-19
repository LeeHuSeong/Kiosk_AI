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
    resultFlag = 0
    optionResult = []
    result = []
    testList = []
    parent = None
    def __init__(self, parent) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

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
        self.btn_start.setText("입력중..")
        self.result = []             #결과
        self.resultFlag = 1     #결과 종류(0: 정확한 결과, 1: 부정확한 결과(리스트), -1: 입력 오류)

        #음성입력 시작

            #여기에 작성 및 result 변수/ resultFlag 변수에 결과 할당

        #음성입력 완료 및 결과반환

        self.btn_start.setText("입력 시작")

        #TEST
        #####

        #결과가 정확하다면
        if self.resultFlag == 0 :
            #result = ['메뉴명', 수량]
            self.result = ['디카페인 아메리카노', 1]
            #menuData = [메뉴이름, 메뉴설명, 메뉴이미지 경로, 옵션리스트, 가격] DB연동
            #menuData = def(result[0])
            menuData = ['디카페인 아메리카노', 'TEST DESCRIPTION', 'img\\drink1\\HOT_디카페인 아메리카노.jpg', ['AddDeShot'], 2500]

            self.stackedWidget.setCurrentIndex(2)

            self.menuStr.setText(menuData[0])   #메뉴이름
            self.menuDesc.setText(menuData[1])  #메뉴설명

            pixmap = QPixmap(menuData[2]).scaled(300, 300)  #메뉴이미지
            self.menuImg.setPixmap(pixmap)
            self.lcdNumber.display(menuData[4])

            self.menuData = [menuData[0], menuData[1], menuData[2], menuData[4], self.result[1]]
            self.optionData = menuData[3]

        #결과가 부정확하다면
        elif self.resultFlag == 1:
            inputStr = '힘들다'
            self.InputStr_2.setText('입력 결과: ' + inputStr)
            #result = [['메뉴명1', '메뉴명2', ...], 수량]
            self.result = [['디카페인 아메리카노', '아메리카노', '디카페인 카페라떼'], 7]

            #menuData = [
                #['메뉴명1', '메뉴설명', '이미지경로', '옵션목록[]', '가격'], 
                #...
            #]
            menuData = [
                ['디카페인 아메리카노', 'TEST DESCRIPTION디카페인아메리카노', 'img\\drink1\\HOT_디카페인 아메리카노.jpg', ['AddDeShot'], 2500], 
                ['아메리카노', 'TEST DESCRIPTION아메리카노', 'img\\drink1\\HOT_아메리카노.jpg', ['AddShot'], 2000],
                ['디카페인 카페라떼', 'TEST DESCRIPTION디카페인카페라떼', 'img\\drink1\\HOT_디카페인 카페라떼.jpg', ['AddDeShot', 'AddLightVanila', 'SelectMilk'], 3900]
            ]

            self.stackedWidget.setCurrentIndex(1)
            #메뉴리스트 ListWidget item으로 반환
            for data in menuData :
                data.append(self.result[1])
                self.addInExactList(data)            

        #오류
        else :
            pass
    
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
        self.aiOptionList.clear()
        #menuData = ['디카페인 아메리카노', 'TEST DESCRIPTION', 'img\\drink1\\HOT_디카페인 아메리카노.jpg', ['AddDeShot', 'AddStevia']]
        #optionResult = [{'AddDeShot': '디카페인 1샷 추가', 'AddStevia': '스테비아 추가'}, 1, '4100원']

        popup_selectOption = front.aiOptionWindow(self.menuData, self.optionData, self)
        popup_selectOption.showModal()

        self.testList = []
        try :
            for key, value in self.optionResult[0].items() :
                self.testList.append(value)
        except :
            pass

        for data in self.testList :
            self.aiOptionList.addItem(data)

        try :
            self.lcdNumber.display(self.optionResult[2])
        except :
            self.lcdNumber.display(self.menuData[3])

    def btn_addCart(self) :
        try :
            data = [self.menuData[0], int(self.optionResult[2]), self.menuData[2], 1, self.testList, self.result[1]]
        except :
            data = [self.menuData[0], self.menuData[3], self.menuData[2], 1, self.testList, self.result[1]]
        #menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg']
        #
        self.parent.addAiCart(data)
        self.close()

    def addInExactList(self, menuData) :
        item_Widget = front.inExactItem(self.aiInExactList, menuData, self)
        item = QListWidgetItem()
        item.setSizeHint(item_Widget.sizeHint())

        self.aiInExactList.addItem(item)
        self.aiInExactList.setItemWidget(item, item_Widget)
    
    def testSleep(self):
        time.sleep(5)