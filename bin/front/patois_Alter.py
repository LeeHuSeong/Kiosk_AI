from openai import OpenAI
import os

class use_OpenAI:
    def gpt_Patois_Correction(text) :
        try :
            client = OpenAI()

            response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "사투리나 부정확한 텍스트를 입력해줄테니 표준어 텍스트로 바꿔줘"},
                {"role": "system", "content": "마침표는 빼고 (온도) 메뉴 수량 형식으로 말해줘"},
                {"role": "user", "content": f"{text}"}
                ]
            )
            result = response.choices[0].message.content
            return result
        
        except Exception as e:
            print(f"gpt_api 키 값이 올바르지 않습니다.\n{e}")
            return text
