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
    def __init__(self, conn, text, synonyms_data):
        self.text = text
        self.synonyms_data = synonyms_data
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
        # 한글 숫자 매핑
        korean_numbers = {
            '한': 1, '두': 2, '세': 3, '네': 4,
            '다섯': 5, '여섯': 6, '일곱': 7, '여덟': 8,
            '아홉': 9, '열': 10, '스물': 20, '서른': 30,
            '마흔': 40, '쉰': 50, '예순': 60, '일흔': 70,
            '여든': 80, '아흔': 90
        }

        def parse_korean_number(korean_str):
            total = 0
            temp = 0
            for char in korean_str:
                if char in korean_numbers:
                    temp += korean_numbers[char]
                elif char == '십':
                    temp = max(1, temp) * 10
            total += temp
            return total

        # 정규식 패턴 (수량과 "잔" 같은 단위를 인식)
        pattern = r'(\d+)|([한두세네다섯여섯일곱여덟아홉열스물서른마흔쉰예순일흔여든아흔십]+)\s*잔'
        matches = re.findall(pattern, self.text)

        total_quantity = 0
        for match in matches:
            if match[0].isdigit():
                total_quantity += int(match[0])
            elif match[1]:
                total_quantity += parse_korean_number(match[1])

        return total_quantity if total_quantity > 0 else 1

    def detect_order_words(self):
        order_keywords = ["주세요", "줘", "주문할게요", "주문"]
        return any(word in self.text for word in order_keywords)


# JSON 데이터 로드
def load_synonyms(file_path="C:/synonyms.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("유사어 데이터 파일을 찾을 수 없습니다.")
        return {}


''' back1 모듈을 가져와서 사용하므로 사용x
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
    conn =create_connection()
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
'''

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


# 사용함수  [ [메뉴이름] , 수량, flag]
def AI_recognition(conn):
    # 유사어 데이터 로드
    synonyms_data = load_synonyms()

    # 음성 인식된 text
    recognized_text = recognize_speech()
    print(recognized_text)

    if recognized_text:
        intent = OrderIntent(conn, recognized_text, synonyms_data)
        intent.extract_menu(conn)

        

        if not intent.menu:
            print("사용 가능한 메뉴와 매칭되지 않았습니다.")
            return [[None],0,0] #메뉴가 없을 때

        #결과 갯수 파악
        result_Flag = 0
        if len(intent.menu) == 1:
            result_Flag=0
        elif len(intent.menu) > 1:
            result_Flag=1
        elif len(intent.menu) < 1:
            result_Flag=-1

        # 결과 출력
        if intent.menu:
            final_result = [[intent.menu], intent.quantity,result_Flag]
            return final_result
        else:
            print("사용 가능한 메뉴와 매칭되지 않았습니다.")
    else:
        print("음성 인식에 실패했습니다.")



#사용함수 ['메뉴이름', '기본가격',  '메뉴이미지 경로', 수량,  옵션리스트, '메뉴 설명']
def get_AI_menu_data(conn):
    try:
        #AI_recognition함수의 리턴값 정보
        # menus = [], quantity = int, flag = int
        menus, quantity, flag = AI_recognition(conn)
        
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
                menu_info        # 메뉴 설명
            ]
            results.append(result)

        return results
    except Exception as e:
        print("get_AI_menu_data ErrorOccured",e)
        return []


'''#test시 사용
#MySQL과 연결
conn=create_connection()
#a = get_menu_option(conn)
#a = AI_recognition(conn)
#a = get_AI_menu_data(conn)

print(a)
'''