# 코드 정리 필요

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

from PyQt5.QtGui import QPixmap

# ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, []]
# ['메뉴이름', '기본가격', '이미지경로', '수량', '옵션리스트']

form_class = uic.loadUiType("bin/front/AIClasses/aiCart_Item.ui")[0]
class aiCartItem(QWidget, form_class) :
    listWidget = None
    # Variables
    menuName = ''           # (STR) 메뉴 이름
    menuDefaultPrice = 0    # (INT) 메뉴 기본가격 
    menuImgSrc = ''         # (STR) 메뉴 이미지 주소
    menuAmount = 1          # (INT) 주문 수량
    menuOption = []         # (LIST[STR]) 선택한 옵션 리스트
    singlePrice = 0         # (INT) 옵션 포함 1개 가격
    totalPrice = 0          # (INT) 옵션 포함 전체 가격

    optionStr = ''          # (STR) Label 출력용 옵션 문자열('\n'.join())

    def __init__(self, listWidget, menuData, parent) :
        super(aiCartItem, self).__init__(parent)
        self.setupUi(self)
        
        self.set_InitData(listWidget, menuData, parent)
        self.set_InitLabelData()

        self.parent.totalPrice += self.totalPrice
        self.parent.lcd_aiPrice.display(self.parent.totalPrice)

    # Initial_Setting
    def set_InitData(self, listWidget, menuData, parent) :  #초기 Class 변수 값 설정
        self.listWidget = listWidget
        self.parent = parent

        self.menuName = menuData[2].split('\\')[2].replace('.jpg', '')
        self.singlePrice = menuData[1]
        self.menuImgSrc = menuData[2]
        self.menuAmount = menuData[3]
        self.menuOption = menuData[4]
        self.set_optionList(menuData[4])

        self.totalPrice = self.singlePrice * self.menuAmount

        if self.menuAmount == 1 :
            self.btn_decrease_menuAmount.setDisabled(True)
        else :
            self.btn_decrease_menuAmount.setEnabled(True)
    
    def set_InitLabelData(self) :       #초기 Label 값 설정
        self.menuName_.setText(self.menuName)
        
        self.menuImg = QPixmap(self.menuImgSrc).scaled(150, 150)
        self.menuPic_.setPixmap(self.menuImg)

        self.optionList_.setText(self.get_optionList())

        self.quantity_.setText(str(self.menuAmount))

        self.itemPrice_.setText(str(self.totalPrice) + '원')

    # getter
    def get_menuName(self) :            #STR
        return self.menuName
    def get_menuImgSrc(self) :          #STR
        return self.menuImgSrc
    def get_menuAmount(self) :          #INT
        return self.menuAmount
    def get_menuOption(self) :          #LIST[STR]
        return self.menuOption
    def get_singlePrice(self) :         #INT
        return self.singlePrice
    def get_totalPrice(self) :          #INT
        return self.totalPrice
    def get_optionList(self) :          #STR
        return self.optionStr

    # setter
    def set_menuAmount(self, value) :   #menuAmount값 value로 설정
        self.menuAmount = value
    def set_optionList(self, list) :    #선택옵션 값 전달/변환
        self.optionStr = '\n'.join(list)

    #def
    def increase_menuAmount(self) :     #menuAmount값 1 증가
        currentAmount = self.get_menuAmount()
        self.menuAmount = currentAmount + 1

        if self.menuAmount == 1 :
            self.btn_decrease_menuAmount.setDisabled(True)
        else :
            self.btn_decrease_menuAmount.setEnabled(True)
            
        self.quantity_.setText(str(self.menuAmount))

        self.parent.totalPrice += self.singlePrice
        self.refresh_totalPrice()

    def decrease_menuAmount(self) :     #menuAmount값 1 감소
        currentAmount = self.get_menuAmount()
        self.menuAmount = currentAmount - 1

        if self.menuAmount == 1 :
            self.btn_decrease_menuAmount.setDisabled(True)
        else :
            self.btn_decrease_menuAmount.setEnabled(True)

        self.quantity_.setText(str(self.menuAmount))

        self.parent.totalPrice -= self.singlePrice
        self.refresh_totalPrice()

        if self.menuAmount == 0 :
            self.remove_item()

    def refresh_totalPrice(self) :      #총 금액 새로고침
        singlePrice = self.get_singlePrice()
        amount = self.get_menuAmount()
        self.totalPrice = singlePrice * amount
        self.itemPrice_.setText(str(self.totalPrice) + '원')

        self.parent.lcd_aiPrice.display(self.parent.totalPrice)

    def remove_item(self) :             #ListWidget에서 제거
        if self.get_menuAmount() != 0 :
            self.parent.totalPrice -= self.get_singlePrice() * self.get_menuAmount()
        
        self.set_menuAmount(0)

        self.parent.Reset_lcd_Price()
        item = self.listWidget.itemAt(self.pos())
        row = self.listWidget.row(item)
        self.listWidget.takeItem(row)#수정

