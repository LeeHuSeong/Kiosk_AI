from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5 import uic

from abc import abstractmethod
import copy

from .cartClass import *
from back1 import get_opt_price

form_class = uic.loadUiType("front/Classes/optionWindowClass.ui")[0]
class optionWindowClass(QDialog, form_class) :
    def __init__(self, parent, conn, menuData, optionResult = None) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        # Var_objectData
        self.__parent = parent
        self.__conn = conn                             # SQL 연결 정보
        self.__menuData = menuData                     # (LIST) 메뉴 전체 데이터
        self.__optionData = menuData[4]                # (LIST) 메뉴 옵션 목록
        
        # Var_menuData
        self.__menuName = menuData[2].split('\\')[2].replace('.jpg', '')    # (STR) 메뉴 이름
        self.__menuDesc = menuData[5]                  # (STR) 메뉴 설명
        self.__menuImgSrc = menuData[2]                # (STR) 메뉴 이미지 주소
        self.__menuDefaultPrice = menuData[1]          # (INT) 메뉴 기본 가격 (옵션 제외 가격)
        self.__menuAmount = menuData[3]                # (INT) 메뉴 주문 수량
        self.__optionPrice = 0                         # (INT) 선택한 옵션 총 가격
        self.__totalPrice = 0                          # (INT) 메뉴 기본 가격 + 선택한 옵션들의 총 가격

        # Var_Others
        self.__optionDict = {                     # (Dict) 버튼 변수
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
        
        # Var_Result
        try :       # 이전 결과 O(음성주문)
            self.__resultNameDict = copy.deepcopy(optionResult[0])     # (Dict) 옵션 선택 결과 Name (옵션 이름/외부 출력용)
            self.__resultIdDict = copy.deepcopy(optionResult[1])       # (Dict) 옵션 선택 결과 ID (옵션 ID/내부 처리용)
            self.__prevNameDict = copy.deepcopy(optionResult[0])       # (Dict) 이전 선택 결과 Name
            self.__prevIdDict = copy.deepcopy(optionResult[1])         # (Dict) 이전 선택 결과 ID
        except :    # 이전 결과 X(일반 주문)
            self.__resultNameDict = {}
            self.__resultIdDict = {}
            self.__prevNameDict = {} 
            self.__prevIdDict = {}

        self.__result = []

        # 라벨 데이터 설정
        self.set_LabelData()

        # 버튼 이벤트 연결/이전 선택내용이 있다면 이전 선택결과 출력
        for key in self.optionDict :
            i = 0
            for value in self.optionDict[key] :
                value.clicked.connect(self.optionSelect)
                try :
                    if key in self.prevIdDict and i == self.prevIdDict[key] :
                        value.setChecked(True)
                except :
                    pass
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

        self.refresh_Price()

    #Getter
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
    def prevNameDict(self) :
        return self.__prevNameDict
    @property
    def prevIdDict(self) :
        return self.__prevIdDict
    @property
    def resultNameDict(self) :
        return self.__resultNameDict
    @property
    def resultIdDict(self) :
        return self.__resultIdDict
    @property
    def optionData(self):
        return self.__optionData
    @property
    def result(self) :
        return self.__result
    #Setter
    @menuAmount.setter  # 메뉴 수량 설정
    def menuAmount(self, Amount) :
        self.__menuAmount = Amount
    @optionPrice.setter # 선택한 옵션 총 가격 설정
    def optionPrice(self, Price) :
        self.__optionPrice = Price
    @totalPrice.setter
    def totalPrice(self, val = None) :
        self.__totalPrice = self.menuDefaultPrice + self.optionPrice
        self.itemPrice_.setText(str(self.totalPrice) + '원')
    @result.setter
    def result(self, val) :
        self.__result = val

    #Methods
    def set_LabelData(self) :   # 라벨 데이터 설정
        self.menuName_.setText(self.menuName)
        self.menuDesc_.setText(self.menuDesc)
        pixmap = QPixmap(self.menuImgSrc).scaled(150, 150)
        self.menuImg_.setPixmap(pixmap)
        self.itemPrice_.setText(str(self.totalPrice) + '원')
    def center(self) :
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def showModal(self) :
        return super().exec_()
    def refresh_Price(self) :   # 옵션버튼 클릭 시 가격 변경
        data = self.resultIdDict.items()
        temp = 0

        if data != {} :
            for key, value in data :
                temp += int(get_opt_price(self.conn, key, value))
        
        self.optionPrice = temp
        self.totalPrice = None

    def optionSelect(self) :
        sender = self.sender()
        getKey = sender
        getValue = sender.objectName()

        key = self.get_key(getKey)
        value = self.get_value(getValue)

        self.resultIdDict[key] = int(value)
        self.refresh_Price()

        self.set_resultNameDict(key, value)
    def set_resultNameDict(self, key, value) :
        options = {
            'Addshot': {1: '1샷 추가', 2: '2샷 추가'},
            'AddDeShot': {1: '디카페인 1샷 추가'},
            'ChangeStevia': {1: '스테비아 변경'},
            'AddStevia': {1: '스테비아 추가'},
            'AddVanila': {1: '바닐라시럽 추가'},
            'ChangeLightVanila': {1: '라이트 바닐라시럽 변경'},
            'AddLightVanila': {1: '라이트 바닐라시럽 추가'},
            'AddCaramel': {1: '카라멜시럽 추가'},
            'SelectMilk': {1: '우유 변경(아몬드)', 2: '우유 변경(오트)'},
            'AddHoney': {1: '꿀 추가'},
            'AddWhipping': {0: '휘핑 빼기', 1: '휘핑 기본'},
            'AddCinnamon': {0: '시나몬 빼기', 1: '시나몬 기본'}
        }
        value = int(value)
        if key in options :
            if value == 0 :
                self.resultNameDict.pop(key, None)
            else:
                self.resultNameDict[key] = options[key].get(value, None)
                # value가 매핑되지 않은 경우 pop으로 제거
                if self.resultNameDict[key] is None:
                    self.resultNameDict.pop(key, None)
    def get_key(self, val) :
        for key in self.optionDict :
            for value in self.optionDict[key]:
                if val == value :
                    return key
    def get_value(self, objectName) :
        return objectName[-1]

    #AbstractMethods
    @abstractmethod
    def btn_Cancel(self) :
        pass

    @abstractmethod
    def btn_OK(self) :
        pass

#일반 주문 옵션 선택 클래스
class optionWindowClass_Default(optionWindowClass) :
    def btn_Cancel(self) :
        self.close()

    def btn_OK(self) :
        self.result = [self.menuName, self.resultNameDict, 1, self.totalPrice]  
        self.close()

#음성 주문 옵션 선택 클래스
class optionWindowClass_Voice(optionWindowClass) :
    def btn_Cancel(self) :
        self.result = [self.prevNameDict, self.prevIdDict, self.totalPrice]
        self.parent.set_optionResult(self.result)    # ai_Dialog 객체로 전달
        self.close()

    def btn_OK(self) :
        self.result = [self.resultNameDict, self.resultIdDict, self.totalPrice]
        self.parent.set_optionResult(self.result)    # ai_Dialog 객체로 전달
        self.close()