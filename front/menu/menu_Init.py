from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import front
import back1

import time #for Test

def menuWidget_Load(self, type) :
        self.menuList.clear()
        menuDB = []
        conn = back1.create_connection()

        if 'menuDB_origin' not in locals()  :
            menuDB_origin = back1.get_menu_price_path_category(conn)    #List
        if 'optionDB' not in locals() :
            optionDB = back1.get_menu_option(conn)                      #Dict

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
    
        menuData = []

        for i in range(0, len(menuDB), 4) :
            menuData.append(menuDB[i:i + 4])

        for itemSet in menuData :
            item_Widget = front.menu_ItemSet(self.menuList, itemSet, self)
            item = QListWidgetItem()
            item.setSizeHint(item_Widget.sizeHint())

            self.menuList.addItem(item)
            self.menuList.setItemWidget(item, item_Widget)

        back1.close_connection(conn)
