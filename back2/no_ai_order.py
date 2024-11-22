import speech_recognition as sr
from bokeh.core.property.primitive import String
import re
import pickle
import back1 as db
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from back1 import *

conn = create_connection()

 # 메뉴 이름
menu_list1=[] # 일반 커피 + 티 + 디저트
menu_list2=[] # 디카페인 커피만

# 음성을 텍스트로 변환하는 함수
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("음성을 입력하세요...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ko-KR");
            print(f"음성 인식 결과: {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("음성을 이해할 수 없습니다.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition 서비스 오류: {e}")
        return None
#메뉴 이름 다 가져옴 (ice, hot 구분없이 이름만 가져오기 위해 where 추가)
def get_menuname1():
    cur = db.cursor(conn)
    sql = "select * from drinks_menu where degree!=%s and category !=%s"
    data=('ICE','디카페인')
    cur.execute(sql,data)
    row = cur.fetchall()
    for i in row:
        #print(i[4])
        menu_list1.append(i[4])
    cur.close()
def get_menuname2():
    cur = db.cursor(conn)
    sql = "select * from drinks_menu where category = %s and degree !=%s"
    data=('디카페인','ICE')
    cur.execute(sql,data)
    row = cur.fetchall()
    for i in row:
        #print(i[4])
        menu_list2.append(i[4])
    cur.close()
#텍스트에 띄어쓰기를 다 없앰
#test=test.replace(' ','')

#음성으로 인식한 텍스트에서 메뉴 이름을 찾아내는 함수
#def check_menu():

#메뉴 이름에 공백 다 제거
#for i in range(len(menu_list)):
 #  menu_list[i] = menu_list[i].replace(" ","")


def check_menu():
    test = '디카페인 아메리카노랑 아메리카노 그리고 카푸치노 또 치즈케익도 주세요'
    #text = recognize_speech()
    get_menuname1()
    get_menuname2()
    if test.find('디카페인')==-1: #음성에 디카페인이 없을 경우 , 디카페인 없는 메뉴 리스트 이용
        print("인식한 메뉴")
        for i in menu_list1:
            if test.find(i)!=-1:
                print(i)
    else: # 음성에 디카페인이 있을 경우
             # 텍스트 복사
        print("인식한 메뉴")
        for i in menu_list2:
            if test.find(i)!=-1:
                test2=test.replace(i,'')
                print(i)
        for i in menu_list1:
            if test2.find(i) != -1:
                print(i)


check_menu()

