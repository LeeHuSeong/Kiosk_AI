import json

# 다양한 주문 문장 패턴 확장
patterns = [
    "{} 한 잔 주세요",
    "{} 두 잔 주세요",
    "{} 세 잔 부탁해요",
    "{} 하나 주문할게요",
    "{} 두 개 주세요",
    "{} 세 개 추가해 주세요",
    "{} 네 잔 주세요",
    "{} 네 개 주세요",
    "{} 한 잔 부탁드립니다",
    "{} 두 잔 부탁드립니다",
    "시원한 {} 한 잔 주세요",
    "따뜻한 {} 두 잔 주세요",
    "{} 하나 더 주세요",
    "{}을/를 주문하고 싶어요",
    "{} 한 잔 바로 부탁해요",
    "{} 추가 주문합니다"
]

# 메뉴 이름 리스트
menu_names = [
    "디카페인 아메리카노", "디카페인 카페라떼", "디카페인 바닐라라떼", "디카페인 연유라떼",
    "디카페인 카라멜마끼아또", "디카페인 카페모카", "디카페인 카푸치노", "아메리카노",
    "카페라떼", "바닐라라떼", "연유라떼", "카라멜마끼야또", "카페모카", "카푸치노",
    "복숭아아이스티", "유자차", "레몬차", "자몽차", "녹차", "캐모마일", "얼그레이",
    "치즈케익", "초코케익", "티라미수케익", "허니브레드"
]

# 수량 매핑 확장
quantity_mapping = {
    "한 잔": "1",
    "두 잔": "2",
    "세 잔": "3",
    "네 잔": "4",
    "하나": "1",
    "두 개": "2",
    "세 개": "3",
    "네 개": "4",
    "하나 더": "1"
}

# 학습 데이터 생성
training_data = []
for menu in menu_names:
    for pattern in patterns:
        input_text = pattern.format(menu)
        # 수량 추출
        for quantity_text, quantity_value in quantity_mapping.items():
            if quantity_text in input_text:
                training_data.append({
                    "input": input_text,
                    "output": {
                        "menu": menu,
                        "quantity": quantity_value
                    }
                })
                break

# JSON으로 변환
json_data = json.dumps(training_data, ensure_ascii=False, indent=4)

# JSON 출력 예시
print(json_data[:500])  # 일부 출력 확인

# JSON 파일로 저장
with open('c:/order_training_data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)
