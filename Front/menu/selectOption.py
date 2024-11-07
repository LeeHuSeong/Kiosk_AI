from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

Order_Class = uic.loadUiType("front/menu/selectOption.ui")[0]

class OrderWindow(QDialog, Order_Class) :
    def __init__(self, menuData, optionData) :
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setupUi(self)
        self.center()

        
        #testMenuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', '디카페인']
        testOptionData = [1, 6, 4, 5, 9, 8]

        self.selectOption_InitSetting(testOptionData)
        #self.parent_mainWindow = parent

        self.selectOption_MenuName.setText(menuData[0])
        self.selectOption_Price.setText(str(menuData[1]) + '원')

        #옵션별 버튼 변수 딕셔너리
        optionDict = {
            'AddShot'           : ['btn_Shot_0', 'btn_Shot_1', 'btn_Shot_2'] ,           #0 샷 추가
            'AddDeShot'         : ['btn_DeShot_0', 'btn_DeShot_1', 'btn_DeShot_2'] ,     #1 디카페인 샷 추가
            'ChangeStevia'      : ['btn_ChangeStev_0', 'btn_ChangeStev_0'] ,             #2 스태비아 변경
            'AddStevia'         : ['btn_ChangeStev_0', 'btn_ChangeStev_0'] ,             #3 스태비아 추가
            'ChangeLightVanila' : ['btn_ChangeLightVan_0', 'btn_ChangeLightVan_1'] ,     #4 라이트 바닐라시럽 변경
            'AddLightVanila'    : ['btn_AddLightVan_0', 'btn_AddLightVan_1'] ,           #5 라이트 바닐라시럽 추가
            'AddVanila'         : ['btn_AddVan_0', 'btn_AddVan_1'] ,                     #6 바닐라시럽 추가
            'AddCaramel'        : ['btn_AddCaramel_0', 'btn_AddCaramel_1'] ,             #7 카라멜시럽 추가
            'SelectMilk'        : ['btn_SelectM_0', 'btn_SelectM_1', 'btn_SelectM_2'] ,  #8 우유 선택
            'AddHoney'          : ['btn_AddHoney_0', 'btn_AddHoney_1'] ,                 #9 꿀 추가
            'AddWhipping'       : ['btn_AddWhip_0', 'btn_AddWhip_1'] ,                   #10 휘핑OX
            'AddCinnamon'       : ['btn_AddCinn_0', 'btn_AddCinn_1']                     #11 시나몬 OX
                     }

    def selectOption_InitSetting(self, optionData) :
        for item in range(0, 12) :
            if item in optionData :
                initStr = 'self.frame_Option_'+str(item)+'.setVisible(True)'
            else :
                initStr = 'self.frame_Option_'+str(item)+'.setVisible(False)'
            eval(initStr)
        


    #창 종료까지 대기
    def showModal(self) :
        return super().exec_()
    
    #창 위치 조정
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
