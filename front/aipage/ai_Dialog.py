from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap
import time

import front
import back1

form_class = uic.loadUiType("front/aipage/ai_Dialog.ui")[0]

class aiDialog(QDialog, form_class) :
    resultFlag = 0
    optionResult = []
    def __init__(self) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        self.aiOptionList = self.aiOptionListWidget
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

        #음성입력 시작
        #self.testSleep()
        #음성입력 완료 및 결과반환

        #self.btn_start.setText("입력 시작")

        self.btn_start.setText("입력 시작")
        result = []         #결과
        resultFlag = 0      #결과 종류(0: 정확한 결과, 1: 부정확한 결과(리스트), -1: 입력 오류)

        #TEST
        #####

        #결과가 정확하다면
        if resultFlag == 0 :
            #menuData = [메뉴이름, 메뉴설명, 메뉴이미지 경로, 옵션리스트, 가격] DB연동
            #menuData = def(result[0])
            menuData = ['디카페인 아메리카노', 'TEST DESCRIPTION', 'img\\drink1\\HOT_디카페인 아메리카노.jpg', ['AddDeShot', 'AddStevia'], 2500]

            self.stackedWidget.setCurrentIndex(2)

            self.menuStr.setText(menuData[0])   #메뉴이름
            self.menuDesc.setText(menuData[1])  #메뉴설명

            pixmap = QPixmap(menuData[2]).scaled(300, 300)  #메뉴이미지
            self.menuImg.setPixmap(pixmap)

            self.menuData = [menuData[0], menuData[1], menuData[2], menuData[4]]
            self.optionData = menuData[3]

        #결과가 부정확하다면
        elif resultFlag == 1:
            pass

        #오류
        else :
            pass
    
    def btn_Back(self) :
        if self.resultFlag == 0 :
            self.stackedWidget.setCurrentIndex(0)
        else :
            self.stackedWidget.setCurrentIndex(1)

    def btn_SelectOption(self) :
        self.aiOptionList.clear()
        #menuData = ['디카페인 아메리카노', 'TEST DESCRIPTION', 'img\\drink1\\HOT_디카페인 아메리카노.jpg', ['AddDeShot', 'AddStevia']]
        #optionResult = [{'AddDeShot': '디카페인 1샷 추가', 'AddStevia': '스테비아 추가'}, 1, '4100원']

        popup_selectOption = front.aiOptionWindow(self.menuData, self.optionData, self)
        popup_selectOption.showModal()

        print(self.menuData)
        print(self.optionResult)
        testList = []
        for key, value in self.optionResult[0].items() :
            testList.append(value)

        print(testList)
        for data in testList :
            self.aiOptionList.addItem(data)

        self.lcdNumber.display(self.optionResult[2])

    def btn_addCart(self) :
        pass
    
    def testSleep(self):
        time.sleep(5)