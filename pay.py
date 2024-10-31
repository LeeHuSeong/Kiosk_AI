import link as data
import pymysql
import numpy as np


conn = pymysql.connect(host='localhost', user='jspuser', password='jsppass',
                       db='jspdb', charset='utf8') #db연결
cur = conn.cursor()

#conn = data.create_connection()
#cur = conn.cursor()



