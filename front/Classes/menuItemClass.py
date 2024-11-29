from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic, QtGui

from .optionWindowClass import optionWindowClass_Default
from .cartClass import cartClass

form_class = uic.loadUiType("front/Classes/menuItemClass.ui")[0]
class menuItemClass(QWidget, form_class) :

    def __init__(self, parent = None) :
        super(menuItemClass, self).__init__(parent)
        self.setupUi(self)

    def menuItem_Init(self, parent, conn, menuData) :
        self.__parent = parent
        self.__conn = conn
        self.__menuData = menuData

        menuNameStr = self.menuData[2].split('\\')[2].replace('.jpg', '').split('_')

        try :
            self.__menuName = menuNameStr[1]            # STR
        except :
            self.__menuName = menuNameStr[0]

        self.__menuImg = QtGui.QIcon(menuData[2])   # QtGui 객체
        self.__Price = menuData[1]                  # INT
        self.__HotIce = menuNameStr[0]              # STR

        self.set_LabelData()

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
    def menuImg(self) :
        return self.__menuImg
    @property
    def menuPrice(self) :
        return self.__Price
    @property
    def HotIce(self) :
        return self.__HotIce 
    
    def set_LabelData(self) :
        self.menuName_.setText(self.menuName)
        self.menuImg_.setIcon(self.menuImg)
        self.menuImg_.setIconSize(QSize(198, 198))
        self.menuPrice_.setText(str(self.menuPrice) + '원')

        if self.HotIce == 'HOT' :
            self.menuHot_.setText(self.HotIce)
        else :
            self.menuIce_.setText(self.HotIce)

    def open_selectOptionPage(self) :
        try :
            self.parent.timer.timeout_Pause()

            selectOptionPage = optionWindowClass_Default(self.parent, self.conn, self.menuData)
            selectOptionPage.showModal()
            result = selectOptionPage.result
            self.parent.timer.timeout_Resume(self.parent.timer.remain_Time)
            cartClass.cartWidget_Add(self.parent, result)
        except :
            pass