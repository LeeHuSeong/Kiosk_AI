from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic


from abc import abstractmethod

form_class = uic.loadUiType("front/aipage/ai_selectOption.ui")[0]
class optionWindowClass(QDialog, form_class) :
    def _init__(self, parent, conn, menuData, optionResult) :
        # Var_objectData
        #self.parent = parent
        self.__conn = conn                             # SQL 연결 정보
        self.__menuData = menuData                     # (LIST) 메뉴 전체 데이터
        self.__optionData = menuData[4]                # (LIST) 메뉴 옵션 목록
        
        # Var_menuData
        self.__menuName = menuData[2].split('\\')[2].replace('.jpg', '') # (STR) 메뉴 이름
        self.__menuDesc = menuData[5]                  # (STR) 메뉴 설명
        self.__menuImgSrc = menuData[2]                # (STR) 메뉴 이미지 주소
        self.__menuDefaultPrice = menuData[1]          # (INT) 메뉴 기본 가격 (옵션 제외 가격)
        self.__menuAmount = menuData[3]                # (INT) 메뉴 주문 수량
        self.__optionPrice = 0                         # (INT) 선택한 옵션 총 가격
        self.__totalPrice = 0                          # (INT) 메뉴 기본 가격 + 선택한 옵션들의 총 가격

        # Var_Others
        self.__optionDict = {                     # 버튼 변수 딕셔너리
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
        self.__prevOptionResult = optionResult    # 이전 선택 결과 딕셔너리 (옵션 ID)
        
        # Var_Result
        self.__resultNameDict = {}    # 옵션 선택 결과 딕셔너리 (옵션 이름/외부 출력용)
        self.__resultIdDict = {}      # 옵션 선택 결과 딕셔너리 (옵션 ID/내부 처리용)

        # 버튼 이벤트 연결/이전 선택내용이 있다면 이전 선택결과 출력
        for key in self.optionDict :
            i = 0
            for value in self.optionDict[key] :
                value.clicked.connect(self.optionSelect)
                if key in self.prevOptionResult[1] and i == self.prevOptionResult[1][key] :
                    value.setChecked(True)
                i += 1

    #Getter
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
    def menuDefaultPrice(self) :
        return self.__menuDefaultPrice
    @property
    def menuAmount(self) :
        return self.__menuAmount
    @property
    def optionPrice(self) :
        return self.__optionPrice
    @property
    def totalPrice(self) :
        return self.__totalPrice
    @property
    def optionDict(self) :
        return self.__optionDict
    @property
    def prevOptionResult(self) :
        return self.__prevOptionResult

    #Setter
    @menuAmount.setter  # 메뉴 수량 설정
    def menuAmount(self, val) :
        if type(val) != int :
            raise TypeError('숫자(정수)만 입력하세요')
        self.__menuAmount = int
    @optionPrice.setter # 선택한 옵션 총 가격 설정
    def optionPrice(self, val) :
        if type(val) != int :
            raise TypeError('숫자(정수)만 입력하세요')
        self.__optionPrice = int
    @totalPrice.setter
    def totalPrice(self) :
        self.__totalPrice = self.menuDefaultPrice + self.optionPrice
    
    def set_LabelData(self) :
        self.menuName_.setText(self.menuName)
        self.menuDesc_.setText(self.menuDesc)
        pixmap = QPixmap(self.menuImgSrc).scaled(150, 150)
        self.menuImg_.setPixmap(pixmap)
        self.itemPrice_.setText(str(self.totalPrice) + '원')

    @abstractmethod
    def something() :
        pass
    
class Car:
    def __init__(self):
        self.__horsepower = 100

    @property
    def horsepower(self):   #getter
        return self.__horsepower

    @horsepower.setter
    def horsepower(self, str): #setter
        self.__horsepower = str