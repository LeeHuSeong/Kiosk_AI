import re
import speech_recognition as sr
import mysql.connector
import pickle
import os

def normalize_dialect_with_model(text, dialect_model, dialect_vectorizer):
    # 방언 모델을 사용하여 텍스트를 표준어로 변환
    vectorized_text = dialect_vectorizer.transform([text])
    normalized_text = dialect_model.predict(vectorized_text)[0]
    print(f"Original Text: {text}")
    print(f"Vectorized Text: {vectorized_text}")
    print(f"Normalized Text after Dialect Processing: {normalized_text}")
    return normalized_text


# 주문 의도를 처리하는 클래스
class OrderIntent:
    def __init__(self, text, order_model, menu_quantity_model, order_vectorizer, menu_quantity_vectorizer, dialect_model, dialect_vectorizer):
        self.text = text
        self.order_model = order_model
        self.menu_quantity_model = menu_quantity_model
        self.order_vectorizer = order_vectorizer
        self.menu_quantity_vectorizer = menu_quantity_vectorizer
        self.dialect_model = dialect_model
        self.dialect_vectorizer = dialect_vectorizer
        self.normalized_text = self.normalize_text()  # 방언 처리
        self.menu = self.extract_menu()  # 메뉴를 DB에서 추출
        self.quantity = self.extract_quantity()  # 수량은 여전히 벡터라이저를 사용
        self.is_order = self.detect_order_words()

    def normalize_text(self):
        # 방언 처리: dialect_model을 사용하여 방언을 표준어로 변환
        normalized_text = normalize_dialect_with_model(self.text, self.dialect_model, self.dialect_vectorizer)
        print(f"Normalized Text after Dialect Processing: {normalized_text}")  # 방언 변환 후 텍스트 출력
        return normalized_text

    def extract_menu(self):
        # 메뉴 이름 가져오기
        menu_names = [menu[0].strip().lower() for menu in get_menu_name()]  # DB에서 메뉴 이름 목록 가져오기
        print(f"Normalized Text: {self.normalized_text}")

        # 메뉴와 정확히 일치하는 항목을 찾는 루프
        for menu in menu_names:
            # 메뉴와 텍스트에 포함된 내용 비교
            if menu in self.normalized_text.lower():  # 부분 일치 검사
                print(f"Found Menu: {menu}")
                return menu

        return None  # 메뉴를 인식하지 못하면 None 반환

    def extract_quantity(self):
        # 수량을 추출하는 로직
        vectorized_text = self.menu_quantity_vectorizer.transform([self.normalized_text])
        predicted_quantity = self.menu_quantity_model.predict(vectorized_text)[0]

        # 예측된 수량이 문자열일 수 있으므로 int로 변환
        try:
            predicted_quantity = int(predicted_quantity)
        except ValueError:
            predicted_quantity = 1  # 예측값이 숫자가 아닐 경우 기본값 1로 설정

        print(f"Extracted Quantity: {predicted_quantity}")
        return max(1, predicted_quantity)  # 최소값 1

    def detect_order_words(self):
        order_keywords = ["주세요", "줘", "주문할게요", "주문"]
        return any(word in self.normalized_text for word in order_keywords)

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
        query = "SELECT 이름 FROM data"  # '이름' 컬럼을 가져온다고 가정
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

# 학습된 모델 로드 및 예측 함수
def load_models():
    model_folder = "model"
    models = {}

    # 모델과 벡터라이저를 함께 로드
    for model_name in ["order_model.pkl", "menu_quantity_model.pkl", "dialect_model.pkl"]:
        model_path = os.path.join(model_folder, model_name)
        if not os.path.exists(model_path):
            print(f"모델 파일이 존재하지 않습니다: {model_name}")
            return None
        with open(model_path, "rb") as model_file:
            models[model_name] = pickle.load(model_file)

    # 각 모델에 대한 벡터라이저도 각각 로드
    order_vectorizer = models["order_model.pkl"][1]  # 주문 모델 벡터라이저
    menu_quantity_vectorizer = models["menu_quantity_model.pkl"][1]  # 메뉴 수량 모델 벡터라이저
    dialect_vectorizer = models["dialect_model.pkl"][1]  # 방언 모델 벡터라이저

    return (
        models["order_model.pkl"][0],  # 주문 모델
        models["menu_quantity_model.pkl"][0],  # 메뉴 수량 모델
        order_vectorizer,
        menu_quantity_vectorizer,
        models["dialect_model.pkl"][0],  # 방언 모델
        dialect_vectorizer
    )

# 실행 코드
recognized_text = recognize_speech()
if recognized_text:
    order_model, menu_quantity_model, order_vectorizer, menu_quantity_vectorizer, dialect_model, dialect_vectorizer = load_models()
    if order_model and menu_quantity_model:
        intent = OrderIntent(recognized_text, order_model, menu_quantity_model, order_vectorizer, menu_quantity_vectorizer, dialect_model, dialect_vectorizer)
        print(f"감지된 주문 문장: {recognized_text}")
        
        if intent.menu:
            print(f"추출된 메뉴: {intent.menu}, 수량: {intent.quantity}")
        else:
            print("메뉴를 인식하지 못했습니다.")
        
        print(f"주문 단어 감지 여부: {'예' if intent.is_order else '아니오'}")
    else:
        print("모델 로드에 실패했습니다.")
else:
    print("음성 인식에 실패했습니다.")
