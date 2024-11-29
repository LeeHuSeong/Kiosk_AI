from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui   


def addShoppingCart(self) :
    optionList = []
    menuPrice = int(self.menuPrice.text().split('\\')[1])
    menuData = [self.menuName.text(), optionList, 1, menuPrice]
        
    self.parent.cartWidget_Add(menuData)
    self.parent.Reset_lcd_Price()
    


    [4400, 
     [
         ['Addshot', []], 
         ['AddDeShot', [['no_choice', '선택x', 0], ['decaffein_shot', '디카페인 샷 추가', 1000]]], 
         ['ChangeStevia', []], 
         ['AddStevia', []], 
         ['ChangeLightVanila', []], 
         ['AddLightVanila', []], 
         ['AddVanila', []], 
         ['AddCaramel', []], 
         ['SelectMilk', [['no_choice', '선택x', 0], ['choose_milk_a', '아몬드밀크변경', 500], ['choose_milk_o', '오트밀크변경', 700]]], 
         ['AddWhipping', [['no_choice', '선택x', 0], ['honey_add', '꿀 추가', 700]]], 
         ['AddCinnamon', []]
     ]
    ]

#장바구니 구조
#변수(자료형)
#  메뉴이름             선택옵션목록            수량      개당 가격
#       menuName(text), optionList(dictionary), amount(int), perPrice
#ex) '디카페인 바닐라라떼', '1: 0, 4: 1, 5: 0, 6: 0, 8: 2, 9: 0', 1, 5400

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
            'AddWhipping'       : ['btn_Whipping_0', 'btn_Whipping_1'] ,                 #10 휘핑OX
            'AddCinnamon'       : ['btn_Cinnamon_0', 'btn_Cinnamon_1']                   #11 시나몬 OX
                     }
    
    self.optionDict = {
            'AddShot'           : [self.btn_Shot_0, self.btn_Shot_1, self.btn_Shot_2] ,             #0 샷 추가
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
    
    '''
    for item in  range(0, 12) :
            if item in optionData :
                initStr = 'self.frame_Option_'+str(item)+'.setVisible(True)'
            else :
                initStr = 'self.frame_Option_'+str(item)+'.setVisible(False)'
            eval(initStr)
    '''







#data = [메뉴이름, 수량, ['디카페인 샷추가', '아몬드밀크 변경'], 총 금액]


'''
if key == 'AddShot' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '1샷 추가'
            elif int(value) == 2 :
                self.selectedOptionDict[key] = '2샷 추가'

        elif key == 'AddDeShot' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '디카페인 1샷 추가'

        elif key == 'ChangeStevia' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '스테비아 변경'
        
        elif key == 'AddStevia' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '스테비아 추가'
        
        elif key == 'AddVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '바닐라시럽 추가'
        
        elif key == 'ChangeLightVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '라이트 바닐라시럽 변경'
        
        elif key == 'AddLightVanila' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '라이트 바닐라시럽 추가'
        
        elif key == 'AddCaramel' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '카라멜시럽 추가'
        
        elif key == 'SelectMilk' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '우유 변경(아몬드)'
            elif int(value) == 2 :
                self.selectedOptionDict[key] = '우유 변경(오트)'
        
        elif key == 'AddHoney' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '꿀 추가'
        
        elif key == 'AddWhipping' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '휘핑 빼기'
        
        elif key == 'AddCinnamon' :
            if int(value) == 0 :
                pass
            elif int(value) == 1 :
                self.selectedOptionDict[key] = '시나몬 빼기'
        
        print(self.selectedOptionDict.items())
        '''


'''

결제창 전달 데이터(리스트)

[
    ['메뉴이름1', [옵션리스트1, 옵션리스트2, ...], 수량, 단일메뉴 총 가격], 
    ['메뉴이름2', [옵션리스트1, 옵션리스트2, ...], 수량, 단일메뉴 총 가격], 
    .
    .
    .
]

예시
[
    ['디카페인 아메리카노', [], 2, 5000], 
    ['디카페인 카페라떼', ['디카페인 1샷 추가', '스테비아 추가'], 2, 11000]
]



'''

#result = ['메뉴명', 수량]
            #self.result = ['디카페인 아메리카노', 7]
            #self.menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, []]
            #self.menuData = [메뉴이름, '기본가격',  메뉴이미지 경로, '수량',  옵션리스트, '메뉴 설명'] DB연동
            #menuData = def(result[0])
            #self.menuData = ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION',]
            #self.menuData = ['디카페인 카페라떼', 3900, 'img\\drink1\\HOT_디카페인 카페라떼.jpg', 1, ['AddDeShot', 'AddLightVanila', 'SelectMilk'], 'TEST DESCRIPTION디카페인카페라떼']

            #menuData = [
                #['메뉴명1', '메뉴설명', '이미지경로', '옵션목록[]', '가격'], 
                #...
            #]
            menuData = [
                ['디카페인 아메리카노', 2500, 'img\\drink1\\HOT_디카페인 아메리카노.jpg', 1, ['AddDeShot'], 'TEST DESCRIPTION디카페인아메리카노'], 
                ['아메리카노', 2000, 'img\\drink1\\HOT_아메리카노.jpg', 1, ['AddShot'], 'TEST DESCRIPTION아메리카노'],
                ['디카페인 카페라떼', 3900,  'img\\drink1\\HOT_디카페인 카페라떼.jpg', 1, ['AddDeShot', 'AddLightVanila', 'SelectMilk'], 'TEST DESCRIPTION디카페인카페라떼']
            ]