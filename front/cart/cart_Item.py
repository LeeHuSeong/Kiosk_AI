from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

#['테스트 메뉴', '옵션 없음', 1, 2000]
#[self.menuName.text(), self.selectedOptionList, 1, self.priceLcd.text()]
cartItem_Class = uic.loadUiType("front/cart/cartItem.ui")[0]

class cartItem(QWidget, cartItem_Class) :
    listWidget = None
    menuData = []
    optionList = []

    menuName = ''
    selectedOptionList = ''
    amount = 0
    singleMenuPrice = 0
    totalMenuPrice = 0

    def __init__(self, listWidget, menuData, parent) :
        super(cartItem, self).__init__(parent)
        self.setupUi(self)
        self.parent = parent

        self.menuData = menuData
        self.listWidget = listWidget
        
        self.menuName = menuData[0]
        

        #print(menuData[1])
        #self.selectedOptionList = '\n'.join(menuData[1])
        optionList = []
        for value in menuData[1].values() :
            optionList.append(value)
        self.optionList = optionList

        self.selectedOptionList = '\n'.join(self.optionList)
        
        self.amount = menuData[2]
        self.singleMenuPrice = int(menuData[3].replace('원', ''))
        self.totalMenuPrice = int(menuData[3].replace('원', ''))

        self.menuName_.setText(menuData[0])
        self.optionList_.setText(self.selectedOptionList)
        self.quantity.setText(str(menuData[2]))
        self.itemPrice.setText(str(self.singleMenuPrice) + '원')

        #print(self.parent.totalPrice)
        self.parent.totalPrice += self.singleMenuPrice
    
    #메뉴 수량 증/감
    def cartItemAmount_Increase(self) :
        self.amount += 1
        self.quantity.setText(str(self.amount))
        self.parent.totalPrice += self.singleMenuPrice

        #self.amount.setText(str(amount))
        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()

    def cartItemAmount_Decrease(self) :
        self.amount -= 1
        self.quantity.setText(str(self.amount))

        if self.amount == 0 :
            self.parent.totalPrice -= self.singleMenuPrice
            self.cartItem_Remove()
        else :
            self.parent.totalPrice -= self.singleMenuPrice

        self.totalMenuPrice = self.singleMenuPrice * self.amount
        self.itemPrice.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()

    #장바구니 메뉴 객체 삭제
    def cartItem_Remove(self) :
        if self.amount == 1 :
            self.parent.totalPrice -= self.singleMenuPrice
            self.amount = 0
        else :
            print(self.singleMenuPrice * self.amount)
            self.parent.totalPrice -= self.singleMenuPrice * self.amount
            self.amount = 0

        self.parent.Reset_lcd_Price()
        item = self.listWidget.itemAt(self.pos())
        row = self.listWidget.row(item)
        self.listWidget.takeItem(row)

    #주문내역 반환
    def get_CartData(self) :
        data = [self.menuName, self.optionList, self.amount, self.totalMenuPrice]
        return data