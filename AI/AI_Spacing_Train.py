# 메뉴 이름 리스트 생성
menu_names = [
    "디카페인 아메리카노", "디카페인 카페라떼", "디카페인 바닐라라떼", "디카페인 연유라떼",
    "디카페인 카라멜마끼아또", "디카페인 카페모카", "디카페인 카푸치노", "아메리카노",
    "카페라떼", "바닐라라떼", "연유라떼", "카라멜마끼야또", "카페모카", "카푸치노",
    "복숭아아이스티", "유자차", "레몬차", "자몽차", "녹차", "캐모마일", "얼그레이",
    "치즈케익", "초코케익", "티라미수케익", "허니브레드"
]
# 다양한 주문 문장 패턴 생성
patterns = [
    "{} 한 잔 주세요",
    "{} 두 잔 주문할게요",
    "저 {} 하나 부탁해요",
    "{} 주세요",
    "{} 추가해 주세요",
    "오늘은 {}로 할게요",
    "시원한 {} 하나 주세요",
    "{} 따뜻하게 하나 부탁해요"
]

# 학습 데이터 생성
training_data = []
for menu in menu_names:
    for pattern in patterns:
        training_data.append(pattern.format(menu))

# 출력 예시
for sentence in training_data[:10]:  # 예제 10개 출력
    print(sentence)
def extract_menu_from_text(text, menu_names):
    for menu in menu_names:
        if menu in text:
            return menu
    return None

# 예제 실행
text = "카페라떼 두 잔 주문할게요"
menu = extract_menu_from_text(text, menu_names)
if menu:
    print(f"인식된 메뉴: {menu}")
else:
    print("메뉴를 인식하지 못했습니다.")
