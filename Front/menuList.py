from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import data_query

def get_db(menuType) :
    db = data_query.menu_price_path()

    if menuType == 'ALL' :
        pass
    elif menuType == 'Decaffein' :
        pass
    elif menuType == 'Coffee' :
        pass
    elif menuType == 'Drinks' :
        pass
    elif menuType == 'Dessert' :
        pass