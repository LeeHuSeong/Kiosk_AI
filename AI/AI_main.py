import re
import speech_recognition as sr
import mysql.connector
import pickle
import os
import json


# 주문 의도를 처리하는 클래스
class OrderIntent:
    def __init__(self, text, synonyms_data, quantity_model):
        self.text = text
        self.synonyms_data = synonyms_data
        self.quantity_model = quantity_model  # 학습된 모델
        self.matched_synonym, self.menu = self.extract_menu()
        self.quantity = self.extract_quantity()
        self.is_order = self.detect_order_words()

    def extract_menu(self):
        # 메뉴 이름 가져오기
        menu_names = [menu.strip().lower() for menu in get_menu_name()]
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

    def extract_quantity(self):
        # 학습된 모델로 수량 예측
        if self.quantity_model:
            model, vectorizer = self.quantity_model
            try:
                transformed_text = vectorizer.transform([self.text])  # 입력 텍스트 변환
                predicted_quantity = model.predict(transformed_text)[0]  # 예측된 수량
                print(f"AI 모델 예측 결과: {predicted_quantity}")
                return predicted_quantity if predicted_quantity > 0 else 1  # 유효성 검사
            except Exception as e:
                print(f"AI 모델 예측 중 오류 발생: {e}")

        # AI 모델 결과가 없을 경우 기본값
        print("AI 모델 예측 실패, 기본값 1로 설정합니다.")
        return 1

    def detect_order_words(self):
        order_keywords = ["주세요", "줘", "주문할게요", "주문"]
        return any(word in self.text for word in order_keywords)


# 학습된 모델 로드
def load_quantity_model(model_path="model/menu_classifier.pkl"):
    if os.path.exists(model_path):
        with open(model_path, "rb") as model_file:
            return pickle.load(model_file)
    else:
        print("학습된 모델 파일을 찾을 수 없습니다.")
        return None



# JSON 데이터 로드
def load_synonyms(file_path="C:/synonyms.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("유사어 데이터 파일을 찾을 수 없습니다.")
        return {}


# MySQL 데이터베이스 연결
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="rootpass",
            database="menu_db"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 오류: {err}")
        return None


# 메뉴 이름 가져오기
def get_menu_name():
    conn = connect_to_db()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        query = "SELECT 이름 FROM data"
        cursor.execute(query)
        result_list = [row[0] for row in cursor.fetchall()]
    except mysql.connector.Error as err:
        print(f"메뉴 가져오기 오류: {err}")
        result_list = []
    finally:
        cursor.close()
        conn.close()

    return result_list


# 음성을 텍스트로 변환하는 함수
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("음성을 입력하세요...")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ko-KR")
            if not text.strip():  # 빈 텍스트 처리
                print("입력된 음성이 없습니다.")
                return None
            print(f"음성 인식 결과: {text}")
            return text.strip()
        except sr.UnknownValueError:
            print("음성을 이해할 수 없습니다.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition 서비스 오류: {e}")
        return None


# 실행 코드
if __name__ == "__main__":
    # 유사어 데이터 로드
    synonyms_data = load_synonyms()

    # 학습된 모델 로드
    quantity_model = load_quantity_model()

    # 음성 인식
    recognized_text = recognize_speech()

    if recognized_text:
        intent = OrderIntent(recognized_text, synonyms_data, quantity_model)

        print(f"감지된 주문 문장: {recognized_text}")

        # 결과 출력
        if intent.menu:
            final_result = [[intent.menu], [intent.quantity]]
            print(f"결과: {final_result}")
        else:
            print("사용 가능한 메뉴와 매칭되지 않았습니다.")
    else:
        print("음성 인식에 실패했습니다.")
