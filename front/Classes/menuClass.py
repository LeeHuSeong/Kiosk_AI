from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .menuItemSetClass import menuItemSetClass
from back1 import get_menu_price_path_category, get_menu_option, get_menu_info

class menuClass :
    def menuWidget_Load(self, conn, type) :
        self.menuList.clear()
        menuDB_origin = get_menu_price_path_category(conn)
        menuDB = []

        optionDB = get_menu_option(conn)                      #Dict

        if type == 'ALL' or type == '' :
            menuDB = menuDB_origin
        else :
            for item in menuDB_origin :
                if item[3] == '커피(ICE)' or item[3] =='커피(HOT)' :
                    menuType = '커피'
                else :
                    menuType = item[3]
                if menuType == type :
                    menuDB.append(item)
                else :
                    pass
                
        for list in menuDB :
            list.append(optionDB[list[0]][1])
            list.pop(3)
            desc = get_menu_info(conn, list[0])
            list.append(desc[0])

            menuData = [menuDB[i:i + 4] for i in range(0, len(menuDB), 4)]

        for itemSet in menuData :
            item_Widget = menuItemSetClass(self, conn, self.menuList, itemSet)
            item = QListWidgetItem()
            item.setSizeHint(item_Widget.sizeHint())
            self.menuList.addItem(item)
            self.menuList.setItemWidget(item, item_Widget)