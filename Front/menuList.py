from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import data_query
#형식: 메뉴이름, 가격, 이미지경로, 분류

def get_db(menuType) :
    db = data_query.get_menu_price_path_category()
    newdb = []
    print(menuType)

    if menuType == 'ALL' :
        newdb = db

    elif menuType == 'Coffee' :
        index = 0

        for item in db :
            if item[3] in ['커피(ICE)', '커피(HOT)'] :
                newdb.append(db[index])
            index += 1

    elif menuType == 'DeCaffeine' :
        index = 0

        for item in db :
            if item[3] in ['디카페인'] :
                newdb.append(db[index])
            index += 1

    elif menuType == 'Drinks' :
        index = 0

        for item in db :
            if item[3] not in ['커피(ICE)', '커피(HOT)', '디카페인', '디저트'] :
                newdb.append(db[index])
            index += 1

    elif menuType == 'Dessert' :
        index = 0

        for item in db :
            if item[3] in ['디저트'] :
                newdb.append(db[index])
            index += 1

    return newdb