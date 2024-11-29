from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

form_class = uic.loadUiType("front/Classes/cartItemClass.ui")[0]

class cartItemClass(QWidget, form_class) :
    def __init__(self, parent, listWidget, menuData) :
        super(cartItemClass, self).__init__(parent)
        self.setupUi(self)
        self.__parent = parent
        self.__listWidget = listWidget
        self.__menuData = menuData
        
        self.__menuName = menuData[0]   

        optionList = []
        for value in menuData[1].values() :
            optionList.append(value)
        self.__optionList = optionList

        self.__selectedOptionList = '\n'.join(self.optionList)
        
        self.__menuAmount = menuData[2]
        self.__menuPrice = menuData[3]
        self.__totalMenuPrice = menuData[3]

        self.set_LabelData()
    
    def set_LabelData(self) :
        self.menuName_.setText(self.menuData[0])
        self.optionList_.setText(self.selectedOptionList)
        self.menuAmount_.setText(str(self.menuAmount))
        self.menuPrice_.setText(str(self.menuPrice) + '원')

        self.btn_cartAmountDec.setDisabled(True)

        self.parent.totalPrice += self.menuPrice

    #Getter
    @property
    def parent(self) :
        return self.__parent
    @property
    def listWidget(self) :
        return self.__listWidget
    @property
    def menuData(self) :
        return self.__menuData
    @property
    def menuName(self) :
        return self.__menuName
    @property
    def optionList(self) :
        return self.__optionList
    @property
    def selectedOptionList(self) :
        return self.__selectedOptionList
    @property
    def menuAmount(self) :
        return self.__menuAmount
    @property
    def menuPrice(self) :
        return self.__menuPrice
    @property
    def totalMenuPrice(self) :
        return self.__totalMenuPrice

    #Setter
    @menuAmount.setter
    def menuAmount(self, val) :
        self.__menuAmount = val
    @totalMenuPrice.setter
    def totalMenuPrice(self, val) :
        self.__totalMenuPrice = val

    def cartItemAmount_Increase(self) :
        self.menuAmount += 1
        print(self.menuAmount)

        if self.menuAmount == 1 :
            self.btn_cartAmountDec.setDisabled(True)
        else :
            self.btn_cartAmountDec.setEnabled(True)
            
        self.menuAmount_.setText(str(self.menuAmount))
        self.parent.totalPrice += self.menuPrice

        self.totalMenuPrice = self.menuPrice * self.menuAmount
        self.menuPrice_.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()

    def cartItemAmount_Decrease(self) :
        self.menuAmount -= 1

        if self.menuAmount == 1 :
            self.btn_cartAmountDec.setDisabled(True)
        else :
            self.btn_cartAmountDec.setEnabled(True)

        self.menuAmount_.setText(str(self.menuAmount))

        if self.menuAmount == 0 :
            self.parent.totalPrice -= self.menuPrice
            self.cartItem_Remove()
        else :
            self.parent.totalPrice -= self.menuPrice

        self.totalMenuPrice = self.menuPrice * self.menuAmount
        self.menuPrice_.setText(str(self.totalMenuPrice) + '원')
        self.parent.Reset_lcd_Price()
    
    def cartItem_Remove(self) :
        if self.menuAmount == 1 :
            self.parent.totalPrice -= self.menuPrice
            self.menuAmount = 0
        else :
            print(self.menuPrice * self.menuAmount)
            self.parent.totalPrice -= self.menuPrice * self.menuAmount
            self.menuAmount = 0

        self.parent.Reset_lcd_Price()
        item = self.listWidget.itemAt(self.pos())
        row = self.listWidget.row(item)
        self.listWidget.takeItem(row)

    def get_CartData(self) :
        data = [self.menuName, self.optionList, self.menuAmount, self.totalMenuPrice]
        return data