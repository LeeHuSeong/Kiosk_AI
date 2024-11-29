import json

# 메뉴 목록
menus = [
    "디카페인 아메리카노", "디카페인 카페라떼", "디카페인 바닐라라떼", "디카페인 연유라떼",
    "디카페인 카라멜마끼아또", "디카페인 카페모카", "디카페인 카푸치노", "아메리카노",
    "카페라떼", "바닐라라떼", "연유라떼", "카라멜마끼야또", "카페모카", "카푸치노",
    "복숭아아이스티", "유자차", "레몬차", "자몽차", "녹차", "캐모마일", "얼그레이",
    "치즈케익", "초코케익", "티라미수케익", "허니브레드"
]

# 수량 표현과 실제 수량 매칭
quantity_phrases = {
    "한잔": 1, "한 잔": 1, "하나": 1, "1잔": 1, "일잔": 1, "한개": 1, "한 개": 1,
    "두 잔": 2, "둘": 2, "2잔": 2, "둘잔": 2, "두잔": 2, "두개": 2, "두 개": 2,
    "세 잔": 3, "셋": 3, "3잔": 3, "셋잔": 3, "세잔": 3, "세개": 3, "세 개": 3,
    "네 잔": 4, "넷": 4, "4잔": 4, "넷잔": 4, "네잔": 4, "네개": 4, "네 개": 4,
    "다섯 잔": 5, "다섯": 5, "5잔": 5, "다섯잔": 5, "다섯개": 5, "다섯 개": 5,
    "여섯 잔": 6, "여섯": 6, "6잔": 6, "여섯잔": 6, "여섯개": 6, "여섯 개": 6,
    "일곱 잔": 7, "일곱": 7, "7잔": 7, "일곱잔": 7, "일곱개": 7, "일곱 개": 7,
    "여덟 잔": 8, "여덟": 8, "8잔": 8, "여덟잔": 8, "여덟개": 8, "여덟 개": 8,
    "아홉 잔": 9, "아홉": 9, "9잔": 9, "아홉잔": 9, "아홉개": 9, "아홉 개": 9,
    "열 잔": 10, "열": 10, "10잔": 10, "열잔": 10, "열개": 10, "열 개": 10
}

# 문장 패턴
sentence_patterns = [
    "{menu} {quantity} 주세요",
    "{menu} {quantity} 부탁드립니다",
    "{menu} {quantity} 원해요",
    "{menu} {quantity} 주문할게요"
]

# 학습 데이터 생성
data = []
for menu in menus:
    for phrase, quantity_value in quantity_phrases.items():
        for pattern in sentence_patterns:
            sentence = pattern.format(menu=menu, quantity=phrase)
            data.append({"sentence": sentence, "quantity": quantity_value})

# JSON 파일로 저장
output_file = "AI/menu_quantity_training_data.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"학습 데이터가 {output_file} 파일로 저장되었습니다.")
