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
        # 한글 숫자 매핑
        korean_numbers = {
        '한': 1, '두': 2, '세': 3, '네': 4,
        '다섯': 5, '여섯': 6, '일곱': 7, '여덟': 8,
        '아홉': 9, '열': 10, '스물': 20, '서른': 30,
        '마흔': 40, '쉰': 50, '예순': 60, '일흔': 70,
        '여든': 80, '아흔': 90
        }

        # 복합 한글 숫자 처리 함수
        def parse_korean_number(korean_str):
            total = 0
            temp = 0
            for char in korean_str:
                if char in korean_numbers:
                    temp += korean_numbers[char]
                elif char == '십':  # '십' 처리
                    temp = max(1, temp) * 10
            total += temp
            return total

        # 정규식 패턴 (수량과 "잔" 같은 단위를 인식)
        pattern = r'\b(\d+)\b|([한두세네다섯여섯일곱여덟아홉열스물서른마흔쉰예순일흔여든아흔십]+)\s*잔'
        matches = re.findall(pattern, self.text)

        # 수량 계산
        total_quantity = 0
        for match in matches:
            if match[0].isdigit():  # 숫자 매칭
                total_quantity += int(match[0])
            elif match[1]:  # 한글 숫자 매칭
                total_quantity += parse_korean_number(match[1])

        return total_quantity if total_quantity > 0 else 1  # 기본값 1



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

    menu_names = get_menu_name()
    if intent.menu in menu_names:
        print(f"매칭된 메뉴: {intent.menu}")
    else:
        print("사용 가능한 메뉴와 매칭되지 않았습니다.")
        print("사용 가능한 메뉴:")
        for menu in menu_names:
            print(f"- {menu}")
else:
    print("음성 인식에 실패했습니다.")
