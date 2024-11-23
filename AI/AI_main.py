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
    def __init__(self, conn, text, dialect_model, synonyms_model, menu_quantity_model, vectorizer):
        self.vectorizer = vectorizer  # vectorizer 초기화
        self.text = self.normalize_text(text, dialect_model)
        self.synonyms_model = synonyms_model
        self.menu_quantity_model = menu_quantity_model
        self.menu = self.extract_menu(conn)
        self.quantity = self.extract_quantity()
        self.is_order = self.detect_order_words()


    def extract_menu(self,conn):
        # 메뉴 이름 가져오기
        menu_names = [menu.strip().lower() for menu in get_menu_name(conn)]

        # 메뉴 직접 매칭
        for menu in menu_names:
            if menu in self.text.lower():
                # 유사어 모델 확인
                vectorized_text = self.vectorizer.transform([menu])
                synonyms = self.synonyms_model.predict(vectorized_text)
                return synonyms[0] if synonyms else menu  # 유사어 모델로부터 예측된 메뉴 반환
        return None

    # 방언 모델을 사용하여 텍스트를 표준어로 변환
    def normalize_text(self, text, dialect_model):
        vectorized_text = self.vectorizer.transform([text])
        normalized_text = dialect_model.predict(vectorized_text)[0]
        return normalized_text
    
    #중첩함수
    def extract_quantity(self):
        # 메뉴와 수량 모델로 수량 예측
        vectorized_text = self.vectorizer.transform([self.text])
        predicted_quantity = self.menu_quantity_model.predict(vectorized_text)[0]
        return max(1, predicted_quantity)  # 최소값 1

    #주문 끝인지 확인
    def detect_order_words(self):
        order_keywords = ["주세요", "줘", "주문할게요", "주문"]
        return any(word in self.text for word in order_keywords)
    


# 학습된 모델 로드 및 예측 함수
def load_models():
    model_folder = "model"
    models = {}

    # 모델과 벡터라이저를 함께 로드
    for model_name in ["dialect_model.pkl", "synonyms_model.pkl", "menu_quantity_and_order_model.pkl"]:
        model_path = os.path.join(model_folder, model_name)
        if not os.path.exists(model_path):
            print(f"모델 파일이 존재하지 않습니다: {model_name}")
            return None
        with open(model_path, "rb") as model_file:
            models[model_name] = pickle.load(model_file)

    # 벡터라이저 로드
    vectorizer = models["dialect_model.pkl"][1]  # 모든 모델이 동일한 벡터라이저를 사용한다고 가정
    return (
        models["dialect_model.pkl"][0],  # 방언 모델
        models["synonyms_model.pkl"][0],  # 유사어 모델
        models["menu_quantity_and_order_model.pkl"][0],  # 메뉴/수량 모델
        vectorizer,
    )

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


# 사용함수  [ [메뉴이름] , 수량, flag]
def AI_recognition(conn):

    # 음성 인식
    recognized_text = recognize_speech()

    if recognized_text:
        dialect_model, synonyms_model, menu_quantity_model, vectorizer = load_models()
        if dialect_model and synonyms_model and menu_quantity_model and vectorizer:
            intent = OrderIntent(recognized_text, dialect_model, synonyms_model, menu_quantity_model, vectorizer)
            print(f"감지된 주문 문장: {recognized_text}")
            #메뉴가 없을때
            if not intent.menu:
                print("사용 가능한 메뉴와 매칭되지 않았습니다.")
                return [[None],0,-1,[recognized_text]] #메뉴가 없을 때

        #결과 갯수 파악
        result_Flag = -1
        if intent.menu:
            if isinstance(intent.menu, list):
                menu_count = len(intent.menu)  # 매칭된 메뉴 개수
            else:
                menu_count = 1  # 단일 메뉴인 경우

        if menu_count == 1:
            result_Flag=0
        elif menu_count > 1:
            result_Flag=1
        elif menu_count < 1:
            result_Flag=-1

        # 결과 출력
        if intent.menu:
            final_result = [[intent.menu], [intent.quantity]]
            print(f"결과: {final_result}")
        else:
            print("사용 가능한 메뉴와 매칭되지 않았습니다.")
    else:
        print("음성 인식에 실패했습니다.")



#사용함수 ['메뉴이름', '기본가격',  '메뉴이미지 경로', 수량,  옵션리스트, '메뉴 설명']
def get_AI_menu_data(conn,menus,quantity,flag):
    try:    
        # 테스트용 변수
        #flag = 1, quantity = 1, menus=["아메리카노","카페라떼"]

        # 플래그 조건에 따른 처리
        if flag == -1: #메뉴가 없을 경우
            print("메뉴가 감지되지 않았습니다.")
            return []
        elif flag == 0:
            menus = [menus[0]]  # 메뉴가 한 개일 경우
        elif flag == 1:
            pass  # 메뉴가 여러 개일 경우
        

        results = [] #메뉴가 여러개일 경우
        
        for menu in menus:
            menu_details = get_menu_price_path_category(conn)
            menu_info = get_menu_info(conn, menu)

            selected_menu_details = next(
                (item for item in menu_details if item[0] == menu), None
            )
            
            #메뉴 정보 추출
            menu_name = selected_menu_details[0]
            base_price = selected_menu_details[1]
            img_path = selected_menu_details[2]

            #옵션 추출
            menu_options = get_menu_option(conn)
            options_origin = menu_options.get(menu_name,[])
            options = options_origin[1] #기본 가격 제외

            result = [
                menu_name,       # 메뉴 이름
                base_price,      # 기본 가격
                img_path,        # 메뉴 이미지 경로
                quantity,        # 수량
                options,         # 옵션 리스트
                menu_info[0]        # 메뉴 설명
            ]
            results.append(result)

        return results
    except Exception as e:
        print("get_AI_menu_data ErrorOccured",e)
        return []


#주의! 아직 학습 데이터 없음
'''#test시 사용
#MySQL과 연결
conn=create_connection()
menu,quantity,flag,text = AI_recognition(conn)
a = get_AI_menu_data(conn,menu, quantity, flag)

#print(menu,quantity,flag, text)
print(a)
'''
