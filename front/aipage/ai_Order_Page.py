from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

AiPage_Class = uic.loadUiType("front/UI/ai_Order_Page.ui")[0]

class aiWindow(QDialog, AiPage_Class) :
    def __init__(self, parent) :
        super(aiWindow, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)

        self.setGeometry(420, 125, 1080, 755)  # x, y, w, h

    def record_Start(self) :
        #녹음시작
        #주문 텍스트 변환 ex) 디카페인 아메리카노 샷추가해서 1잔

        rawText = ''        # AI처리 전 입력 텍스트
        resultText = ''     # AI처리 후 변환된 텍스트

        return resultText   #텍스트 변환 결과

    def load_orderData(self) :
        #DB조회 및 메뉴데이터 + 옵션데이터 반환
        #ex) [ '디카페인 아메리카노', '메뉴가격', '이미지경로', '옵션정보' ]
        #           옵션정보: [샷추가 ]
        pass
