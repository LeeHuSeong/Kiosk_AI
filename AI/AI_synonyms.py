import re
import speech_recognition as sr
import mysql.connector
import pickle
import os


# 주문 의도를 처리하는 클래스
class OrderIntent:
    def __init__(self, text):
        self.text = text
        self.menu = self.extract_menu()
        self.quantity = self.extract_quantity()
        self.is_order = self.detect_order_words()

    def extract_menu(self):
        menu_names = [menu.strip().lower() for menu in get_menu_name()]  # 공백 제거 및 소문자 통일
        for menu in menu_names:
            if menu in self.text.lower():  # 입력 텍스트도 소문자로 통일
                return menu
        return None

    def extract_quantity(self):
        quantity_pattern = re.findall(r'\b(\d+)\b|[한두세네다섯여섯일곱여덟아홉열]', self.text)
        if quantity_pattern:
            korean_numbers = {
                '한': 1, '두': 2, '세': 3, '네': 4,
                '다섯': 5, '여섯': 6, '일곱': 7, '여덟': 8,
                '아홉': 9, '열': 10
            }
            quantities = [
                int(num) if num.isdigit() else korean_numbers.get(num, 0)
                for num in quantity_pattern
            ]
            return sum(quantities)  # 모든 매칭된 수량을 합산
        return 1  # 기본값은 1

    def detect_order_words(self):
        order_keywords = ["주세요", "줘", "주문할게요", "주문"]
        return any(word in self.text for word in order_keywords)


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


# 메뉴 주문 카운트 증가
def update_order_count(menu):
    conn = connect_to_db()
    if conn is None:
        return None

    try:
        cursor = conn.cursor()
        query = "UPDATE orders SET count = count + 1 WHERE menu = %s"
        cursor.execute(query, (menu,))
        conn.commit()

        query_today = "SELECT SUM(count) FROM orders WHERE DATE(order_time) = CURDATE()"
        cursor.execute(query_today)
        order_count_today = cursor.fetchone()[0] or 0
    except mysql.connector.Error as err:
        print(f"쿼리 실행 오류: {err}")
        order_count_today = None
    finally:
        cursor.close()
        conn.close()

    return order_count_today


# 학습된 모델 로드 및 예측 함수
def load_model(model_path="model/menu_classifier.pkl"):
    if not os.path.exists(model_path):
        print("모델 파일이 존재하지 않습니다.")
        return None, None, None

    with open(model_path, "rb") as model_file:
        model, vectorizer, synonyms_data = pickle.load(model_file)
    return model, vectorizer, synonyms_data


# 실행 코드
recognized_text = recognize_speech()

if recognized_text:
    intent = OrderIntent(recognized_text)

    print(f"감지된 주문 문장: {recognized_text}")
    print(f"추출된 메뉴: {intent.menu if intent.menu else '메뉴를 인식하지 못했습니다.'}")
    print(f"추출된 수량: {intent.quantity}")
    print(f"주문 단어 감지 여부: {'예' if intent.is_order else '아니오'}")

    model, vectorizer, synonyms_data = load_model()

    if model and vectorizer:
        processed_text = recognized_text.lower().strip()
        X = vectorizer.transform([processed_text])
        predicted_menu = model.predict(X)[0]

        menu_names = get_menu_name()
        if predicted_menu in menu_names:
            print(f"선택된 메뉴: {predicted_menu}")
            order_count_today = update_order_count(predicted_menu)
            if order_count_today is not None:
                print(f"오늘의 {order_count_today}번째 주문입니다.")
            else:
                print("주문 카운트 업데이트에 실패했습니다.")
        else:
            print("메뉴를 인식하지 못했습니다.")
    else:
        print("모델을 로드할 수 없습니다.")
else:
    print("음성 인식에 실패했습니다.")
