from openai import OpenAI
import os

class use_OpenAI:
    def __init__(self, text):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        client = OpenAI()

        response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "주문할 텍스트를 적어줄테니 [[ICE/HOT, '메뉴이름'], 수량]의 형식(파이썬 리스트)으로 변환해줘"},
            {"role": "user", "content": f"{text}"}
            ]
        )
        result = response.choices[0].message.content
        return result
        