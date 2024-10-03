#음성인식 라이브러리 설치
#pip install SpeechRecognition


import re
import speech_recognition as sr

# 예시 메뉴 리스트
menu_list = ["아메리카노", "라떼", "카푸치노"]

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

# 음성 인식 후 메뉴를 추출
recognized_text = recognize_speech()

if recognized_text:
    selected_menu = extract_menu(recognized_text, menu_list)
    
    if selected_menu:
        print(f"선택된 메뉴: {selected_menu}")
    else:
        print("메뉴를 인식하지 못했습니다.")
else:
    print("음성 인식에 실패했습니다.")
