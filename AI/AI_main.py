import re
import speech_recognition as sr
import mysql.connector
import pickle
import os
import json
from sklearn.feature_extraction.text import CountVectorizer


class OrderIntent:
    def __init__(self, text, synonyms_data, menu_quantity_model, menu_quantity_vectorizer):
        self.text = text
        self.synonyms_data = synonyms_data
        self.menu_quantity_model = menu_quantity_model
        self.menu_quantity_vectorizer = menu_quantity_vectorizer
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


# 실행 코드
if __name__ == "__main__":
    # 유사어 데이터 로드
    synonyms_data = load_synonyms()

    # 음성 인식
    recognized_text = recognize_speech()

    if recognized_text:
        menu_quantity_model, menu_quantity_vectorizer = load_models()
        if menu_quantity_model and menu_quantity_vectorizer:
            intent = OrderIntent(recognized_text, synonyms_data, menu_quantity_model, menu_quantity_vectorizer)

            # 유사어 리스트 감지 시
            if intent.matched_synonym:
                # 매칭된 키에 포함된 메뉴 리스트를 결과에 포함
                matched_menu_list = synonyms_data[intent.matched_synonym]
                result = [[matched_menu_list], [intent.quantity]]
            else:
                # 메뉴 이름과 수량만 포함
                result = [[intent.menu], [intent.quantity]]

            # 결과 출력
            print(f"감지된 음성: {recognized_text}")
            print(f"출력 결과: {result}")
        else:
            print("모델 로드에 실패했습니다.")
    else:
        print("음성 인식에 실패했습니다.")
