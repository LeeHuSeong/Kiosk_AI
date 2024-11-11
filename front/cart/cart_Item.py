from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

#data = ['테스트 메뉴', '옵션 없음', 1, 2000]

form_class = uic.loadUiType("front/cart/cartItem.ui")[0]
cart_List = []

class cartItem(QWidget, form_class) :
    list_Widget = None
    allPrice = 0
    def __init__(self, list_Widget, data, totalPrice) :
        self.allPrice = totalPrice
        print(self.allPrice)
        self.data = data
        self.list_Widget = list_Widget

        super().__init__()
        self.setupUi(self)

        self.menuName.setText(data[0])

        optionList = ''.join(data[1])
        self.optionList.setText(optionList)
        self.amount.setText('1')
        self.itemPrice.setText(str(data[2]))
        self.allPrice += data[2]
        print("data[2]1 : " + str(data[2]))

    def cartItemAmount_Increase(self) :

        amount = int(self.amount.text())
        amount += 1
        self.amount.setText(str(amount))

    def cartItemAmount_Decrease(self) :
        
        amount = int(self.amount.text())
        amount -= 1

        if amount == 0 :
            self.cartItem_Remove()

        self.amount.setText(str(amount))

    def cartItem_Add(self, data) :
        if data[0] == 'defaultImage.jpg' :
            pass
        else :
            item_widget = cartItem(self.list_Widget, data, self.allPrice)

            item = QListWidgetItem()
            item.setSizeHint(item_widget.sizeHint())
            item.setFlags(Qt.ItemIsEnabled)

            self.list_Widget.addItem(item)
            self.list_Widget.setItemWidget(item, item_widget)
            print("data[2]2 : " + str(data[2]))

        #print(data[0])
    
    def cartItem_Remove(self) :
        item = self.list_Widget.itemAt(self.pos())
        row = self.list_Widget.row(item)
        self.list_Widget.takeItem(row)

    def cartItem_Reset(self) :
        self.list_Widget.clear()
        self.allPrice = 0

    def update_AllPrice(self) :
        print("self.allPrice : " + str(self.allPrice))