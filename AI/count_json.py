import json

# 메뉴 목록
menus = [
    "디카페인 아메리카노", "디카페인 카페라떼", "디카페인 바닐라라떼", "디카페인 연유라떼",
    "디카페인 카라멜마끼아또", "디카페인 카페모카", "디카페인 카푸치노", "아메리카노",
    "카페라떼", "바닐라라떼", "연유라떼", "카라멜마끼야또", "카페모카", "카푸치노",
    "복숭아아이스티", "유자차", "레몬차", "자몽차", "녹차", "캐모마일", "얼그레이",
    "치즈케익", "초코케익", "티라미수케익", "허니브레드"
]

# 수량 표현
quantity_phrases = [
    "한잔", "한 잔", "하나", "1잔", "일잔", 
    "두 잔", "둘", "2잔", "둘잔", "두잔",
    "세 잔", "셋", "3잔", "셋잔", "세잔",
    "네 잔", "넷", "4잔", "넷잔", "네잔",
    "다섯 잔", "다섯", "5잔", "다섯잔", "다섯개",
    "여섯 잔", "여섯", "6잔", "여섯잔", "여섯개",
    "일곱 잔", "일곱", "7잔", "일곱잔", "일곱개",
    "여덟 잔", "여덟", "8잔", "여덟잔", "여덟개",
    "아홉 잔", "아홉", "9잔", "아홉잔", "아홉개",
    "열 잔", "열", "10잔", "열잔", "열개"
]

# 학습 데이터 생성
data = []
for menu in menus:
    quantity = 1  # 초기 수량
    for i, phrase in enumerate(quantity_phrases, start=1):
        sentence = f"{menu} {phrase} 주세요"
        data.append({"sentence": sentence, "quantity": quantity})
        if i % 10 == 0:  # 수량을 10개씩 그룹으로 증가
            quantity += 1

# JSON 파일로 저장
output_file = "menu_quantity_training_data.json"
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

print(f"학습 데이터가 {output_file} 파일로 저장되었습니다.")
