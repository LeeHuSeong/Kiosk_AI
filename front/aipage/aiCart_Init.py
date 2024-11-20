from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import front

def aiCartWidget_Add(self, menuData) :
    item_Widget = front.aiCartItem(self.aiCartList, menuData, self)
    item = QListWidgetItem()
    item.setSizeHint(item_Widget.sizeHint())

    self.aiCartList.addItem(item)
    self.aiCartList.setItemWidget(item, item_Widget)