import re
import speech_recognition as sr
import mysql.connector
import pickle

# MySQL 데이터베이스 연결
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="rootpass",
        database="menu_db"
    )
    return connection

# 음성을 텍스트로 변환하는 함수
def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # 주변 소음 조정
        print("음성을 입력하세요...")
        audio = recognizer.listen(source)

        try:
            # Google API를 사용해 음성 인식을 수행
            text = recognizer.recognize_google(audio, language="ko-KR")
            print(f"음성 인식 결과: {text}")
            return text
        except sr.UnknownValueError:
            print("음성을 이해할 수 없습니다.")
        except sr.RequestError as e:
            print(f"Google Speech Recognition 서비스 오류: {e}")
        return None

# 메뉴 주문 카운트 증가
def update_order_count(menu):
    conn = connect_to_db()
    cursor = conn.cursor()

    # 메뉴의 주문 횟수 증가
    query = "UPDATE orders SET count = count + 1 WHERE menu = %s"
    cursor.execute(query, (menu,))
    conn.commit()

    # 오늘의 몇 번째 주문인지 확인
    query_today = "SELECT SUM(count) FROM orders WHERE DATE(order_time) = CURDATE()"
    cursor.execute(query_today)
    order_count_today = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return order_count_today

# 학습된 모델 로드 및 예측 함수
def load_model():
    with open("menu_classifier.pkl", "rb") as model_file:
        model, vectorizer = pickle.load(model_file)
    return model, vectorizer

def classify_menu(text, model, vectorizer):
    X = vectorizer.transform([text])
    predicted_menu = model.predict(X)
    return predicted_menu[0]

# 음성 인식 후 메뉴를 추출
recognized_text = recognize_speech()

if recognized_text:
    # 학습된 모델 로드
    model, vectorizer = load_model()
    
    # 텍스트를 기반으로 메뉴 분류
    selected_menu = classify_menu(recognized_text, model, vectorizer)

    if selected_menu:
        print(f"선택된 메뉴: {selected_menu}")
        
        # 주문 카운트 업데이트 및 오늘의 주문 수 출력
        order_count_today = update_order_count(selected_menu)
        print(f"오늘의 {order_count_today}번째 주문입니다.")
    else:
        print("메뉴를 인식하지 못했습니다.")
else:
    print("음성 인식에 실패했습니다.")
