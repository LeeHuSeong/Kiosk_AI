import speech_recognition as sr
import mysql.connector
import pickle
import os

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

    cursor = conn.cursor()
    try:
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


def classify_menu(text, model, vectorizer):
    if model is None or vectorizer is None:
        return None
    
    X = vectorizer.transform([text])
    predicted_menu = model.predict(X)
    return predicted_menu[0] if predicted_menu else None

# 실행 코드
recognized_text = recognize_speech()

if recognized_text:
    # 학습된 모델과 유사어 데이터 로드
    model, vectorizer, synonyms_data = load_model()

    # 텍스트를 기반으로 메뉴 분류
    selected_menu = classify_menu(recognized_text, model, vectorizer)

    if selected_menu:
        print(f"선택된 메뉴: {selected_menu}")

        # 선택된 메뉴에 매칭되는 유사어 리스트 출력
        if selected_menu in synonyms_data:
            print(f"{selected_menu}의 유사어 리스트: {synonyms_data[selected_menu]}")
        else:
            print("해당 메뉴에 대한 유사어가 없습니다.")
        
        # 주문 카운트 업데이트 및 오늘의 주문 수 출력
        order_count_today = update_order_count(selected_menu)
        if order_count_today is not None:
            print(f"오늘의 {order_count_today}번째 주문입니다.")
        else:
            print("주문 카운트 업데이트에 실패했습니다.")
    else:
        print("메뉴를 인식하지 못했습니다.")
else:
    print("음성 인식에 실패했습니다.")

