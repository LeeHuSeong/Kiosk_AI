import re
import speech_recognition as sr
import mysql.connector
import pickle
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')
from back1 import *


# 주문 의도를 처리하는 클래스
class OrderIntent:
    def __init__(self,conn, text, synonyms_data, menu_quantity_model, menu_quantity_vectorizer):
        self.text = text
        self.synonyms_data = synonyms_data
        self.menu_quantity_model = menu_quantity_model
        self.menu_quantity_vectorizer = menu_quantity_vectorizer
        self.matched_synonym, self.menu = self.extract_menu(conn)
        self.quantity = self.extract_quantity()
        self.is_order = self.detect_order_words()


    def extract_menu(self,conn):
        # 메뉴 이름 가져오기
        menu_names = [menu.strip().lower() for menu in get_menu_name(conn)]
        text_lower = self.text.lower()

        # 메뉴 직접 매칭
        for menu in menu_names:
            if menu in text_lower:
                return None, menu

        # 유사어 검색 (길이가 긴 키워드 우선 매칭)
        matched_key = None
        for key in sorted(self.synonyms_data.keys(), key=len, reverse=True):
            if key in text_lower:
                matched_key = key
                break

        if matched_key:
            return matched_key, self.synonyms_data[matched_key]

        return None, None

    #중첩함수
    def extract_quantity(self):
        # 한글 수량과 숫자를 매핑하는 사전
        korean_to_number = {
            "한": 1, "두": 2, "세": 3, "네": 4, "다섯": 5,
            "여섯": 6, "일곱": 7, "여덟": 8, "아홉": 9, "열": 10
        }

        # 텍스트에서 한글 수량 또는 숫자 수량 추출
        text_lower = self.text.lower()
        quantity = 1  # 기본값

        # 한글 수량 처리
        for korean, num in korean_to_number.items():
            if korean in text_lower:
                quantity = num
                break

        # 숫자 수량 처리 (숫자가 우선)
        number_match = re.search(r"(\d+)", self.text)
        if number_match:
            quantity = int(number_match.group(1))

        # 머신러닝 모델 사용
        try:
            vectorized_text = self.menu_quantity_vectorizer.transform([self.text])
            predicted_quantity = self.menu_quantity_model.predict(vectorized_text)[0]
            print(f"[DEBUG] 모델 예측 수량: {predicted_quantity}")
            return max(quantity, int(predicted_quantity))  # 모델과 추출한 수량 중 더 큰 값을 사용
        except Exception as e:
            print(f"[ERROR] 수량 예측 오류: {e}")
            return quantity

    def detect_order_words(self):
        order_keywords = ["주세요", "줘", "주문할게요", "주문"]
        return any(word in self.text for word in order_keywords)


# JSON 데이터 로드
def load_synonyms(file_path="AI/synonyms.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("유사어 데이터 파일을 찾을 수 없습니다.")
        return {}


# 음성을 텍스트로 변환하는 함수
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("음성을 입력하세요...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
            print(f"음성 인식 결과: {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("음성을 이해할 수 없습니다.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition 서비스 오류: {e}")
        return None

# 학습된 모델 로드
def load_models():
    model_folder = "model"
    try:
        with open(os.path.join(model_folder, "menu_classifier.pkl"), "rb") as file:
            menu_quantity_model, menu_quantity_vectorizer = pickle.load(file)
        return menu_quantity_model, menu_quantity_vectorizer
    except FileNotFoundError:
        print("모델 파일을 찾을 수 없습니다.")
        return None, None


# 사용함수  [ [메뉴이름] , 수량, flag,[text]]
def AI_recognition(conn):
    # 유사어 데이터 로드
    synonyms_data = load_synonyms()

    # 음성 인식된 text
    recognized_text = recognize_speech()

    #메뉴 갯수 파악하는 변수
    result_flag=-1

    if recognized_text:
        menu_quantity_model, menu_quantity_vectorizer = load_models()
        if menu_quantity_model and menu_quantity_vectorizer:
            intent = OrderIntent(conn ,recognized_text, synonyms_data, menu_quantity_model, menu_quantity_vectorizer)

        # 유사어 리스트 감지 시
        if intent.matched_synonym:
            # 매칭된 키에 포함된 메뉴 리스트를 결과에 포함
            matched_menu_list = synonyms_data[intent.matched_synonym]
            result_flag=1
            if isinstance(matched_menu_list, list) and any(isinstance(i, list) for i in matched_menu_list):
                matched_menu_list = [item for sublist in matched_menu_list for item in sublist]  # 리스트 평탄화
            return [matched_menu_list, intent.quantity,result_flag,recognized_text]
       
        #메뉴가 없을때
        elif intent.menu:
            result_flag=0
            return [[intent.menu],intent.quantity,result_flag,recognized_text] #메뉴가 없을 때

        else:
            result_flag = -1
            print("사용 가능한 메뉴와 매칭되지 않았습니다.")
            return [[None],0,result_flag,recognized_text] #메뉴가 없을 때
    else:
        print("음성 인식에 실패했습니다.")
        return [[None],0,result_flag,None]



#사용함수 ['메뉴이름', '기본가격',  '메뉴이미지 경로', 수량,  옵션리스트, '메뉴 설명']
def get_AI_menu_data(conn, menu, amount):
    try:    
        menuData = get_menu_totalData(conn, menu)

        if amount < 1 :
            Amount = 1
        else :
            Amount = amount
        
        #메뉴 정보 추출
        menu_name = menuData[0]
        base_price = menuData[1]
        img_path = menuData[2]
        menu_info = menuData[4]
        #옵션 추출
        menu_options = get_menu_option(conn)
        options_origin = menu_options.get(menu_name, [])
        options = options_origin[1] #if len(options_origin) > 1 else [] #기본 가격 제외

        result = [
            menu_name,      # 메뉴 이름
            base_price,     # 기본 가격
            img_path,       # 메뉴 이미지 경로
            Amount,         # 수량 
            options,        # 옵션 리스트
            menu_info       # 메뉴 설명
        ]

        #print(f"get_AI_menu_data: {result}")
        return result
    
    except Exception as e:
        print("get_AI_menu_data ErrorOccured",e)
        return []


##test시 사용
##MySQL과 연결
#conn=create_connection()

#menu,quantity,flag,text = AI_recognition(conn)
#a = get_AI_menu_data(conn,menu, quantity, flag)
#print(menu,quantity,flag, text)
#print(a)
#print(AI_recognition(conn))
