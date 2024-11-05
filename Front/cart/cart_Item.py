from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

#data = ['테스트 메뉴', '옵션 없음', 1, 2000]

form_class = uic.loadUiType("front/cart/cartItem.ui")[0]
item_List = []

class cartItem(QWidget, form_class) :
    parent = None
    list_Widget = None
    def __init__(self, list_Widget, data) :
        self.data = data
        self.list_Widget = list_Widget

        super().__init__()
        self.setupUi(self)

        self.menuName.setText(data[0])
        self.optionList.setText(data[1])
        self.amount.setText(str(data[2]))
        self.itemPrice.setText(str(data[3]))

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
        item_widget = cartItem(self.list_Widget, data)

        item = QListWidgetItem()
        item.setSizeHint(item_widget.sizeHint())
        item.setFlags(Qt.ItemIsEnabled)

        self.list_Widget.addItem(item)
        self.list_Widget.setItemWidget(item, item_widget)

        item_List.append(item)

        return item
    
    def cartItem_Remove(self) :
        item = self.list_Widget.itemAt(self.pos())
        row = self.list_Widget.row(item)
        self.list_Widget.takeItem(row)
