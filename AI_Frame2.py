#각각 설치 필요
#pip install SpeechRecognition << 음성 받는거
#conda install -c anaconda pyaudio << SpeechRecognition 사용에 필요
#conda install -c anaconda mysql-connector-python << sql connector

import re
import speech_recognition as sr
import mysql.connector

# 예시 메뉴 리스트
menu_list = ["아메리카노", "라떼", "카푸치노", "커피", "카페라떼", "바닐라라떼", "연유라떼", "카라멜마끼아또", "카페모카", "시나몬", "캐모마일", "얼그레이", "복숭아아이스티"]

# MySQL 데이터베이스 연결
def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",        # 본인의 DB 사용자 이름으로 수정
        password="rootpass", # 본인의 DB 비밀번호로 수정
        database="menu_db"  # 본인의 DB 이름으로 수정
    )
    return connection

# 음성 인식 후 텍스트에서 메뉴를 추출하는 함수
def extract_menu(text, menu_list):
    for menu in menu_list:
        if re.search(menu, text):
            return menu
    return None

# 음성을 텍스트로 변환하는 함수
def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("음성을 입력하세요...")
        audio = recognizer.listen(source)

        try:
            # Google API를 사용해 음성 인식을 수행
            text = recognizer.recognize_google(audio, language="ko-KR")  # 한국어로 설정
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

# 음성 인식 후 메뉴를 추출
recognized_text = recognize_speech()

if recognized_text:
    selected_menu = extract_menu(recognized_text, menu_list)
    
    if selected_menu:
        print(f"선택된 메뉴: {selected_menu}")
        
        # 주문 카운트 업데이트 및 오늘의 주문 수 출력
        order_count_today = update_order_count(selected_menu)
        print(f"오늘의 {order_count_today}번째 주문입니다.")
    else:
        print("메뉴를 인식하지 못했습니다.")
else:
    print("음성 인식에 실패했습니다.")
