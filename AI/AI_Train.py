import os
import pickle
import json
import re
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer


class CustomModelTrainer:
    def __init__(self, data_folders, model_folder="model", pretrained_model_folder="model"):
        self.data_folders = data_folders  # 데이터 폴더
        self.model_folder = model_folder  # 모델 저장 폴더
        self.pretrained_model_folder = pretrained_model_folder  # 사전 훈련된 모델 폴더
        self.vectorizer = None  # 벡터라이저
        self.models = {}  # 여러 모델을 저장할 딕셔너리

        # 모델 폴더가 존재하지 않으면 생성
        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)
            print(f"[INFO] 모델 저장 폴더 생성: {self.model_folder}")
        else:
            print(f"[INFO] 모델 저장 폴더 존재: {self.model_folder}")

        # 사전 훈련된 벡터라이저 로드
        self.load_vectorizer()

    def load_vectorizer(self):
        """사전 훈련된 벡터라이저를 불러오는 함수"""
        vectorizer_path = os.path.join(self.pretrained_model_folder, "vectorizer.pkl")
        if os.path.exists(vectorizer_path):
            with open(vectorizer_path, "rb") as vectorizer_file:
                self.vectorizer = pickle.load(vectorizer_file)
            print(f"[INFO] 사전 훈련된 벡터라이저 불러오기 완료: {vectorizer_path}")
        else:
            print("[WARNING] 사전 훈련된 벡터라이저가 존재하지 않습니다. 새로 생성합니다.")
            self.vectorizer = CountVectorizer()  # 새 벡터라이저 초기화

    def load_data(self, file_path):
        """데이터를 JSON 형식으로 로드"""
        if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
            print(f"[WARNING] 파일이 비어 있거나 존재하지 않습니다: {file_path}")
            return {}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSONDecodeError: {file_path} 파일 읽기 오류: {e}")
            return {}

    def clean_text(self, text):
        """텍스트를 정제하는 함수"""
        text = text.lower()  # 소문자화
        text = re.sub(r'[^\w\s]', '', text)  # 알파벳, 숫자, 공백만 남기기
        return text.strip()

    def train_model(self, data, model_filename):
        """주어진 데이터를 바탕으로 모델 학습"""
        texts = []
        labels = []

        if isinstance(data, dict):  # synonyms.json 또는 유사 구조 처리
            for key, values in data.items():
                for value_set in values:
                    texts.append(" ".join(value_set))  # 여러 값을 공백으로 구분한 텍스트로 변환
                    labels.append(key)  # 키는 레이블로 사용
        elif isinstance(data, list):  # order_training_data 또는 menu_quantity_training_data 처리
            for item in data:
                if "input" in item and "output" in item:  # order_training_data 구조
                    texts.append(item["input"])
                    # 'output'에서 'menu'와 'quantity'를 분리하여 레이블로 추가
                    menu = item["output"].get("menu", "")
                    quantity = item["output"].get("quantity", "")
                    labels.append(f"{menu}_{quantity}")  # 레이블을 'menu_quantity' 형태로 저장
                elif "sentence" in item and "quantity" in item:  # menu_quantity_training_data 구조
                    texts.append(item["sentence"])
                    labels.append(str(item["quantity"]))

        print(f"[INFO] 학습에 사용되는 텍스트 개수: {len(texts)}")
        print(f"[INFO] 학습에 사용되는 레이블 개수: {len(labels)}")

        if len(texts) == 0:
            print(f"[ERROR] 학습에 사용되는 텍스트가 없습니다!")
            return

        # 빈 텍스트 필터링 및 정제
        filtered_texts = [self.clean_text(text) for text in texts if text.strip() != ""]
        print(f"[INFO] 정제 후 텍스트 개수: {len(filtered_texts)}")

        if len(filtered_texts) == 0:
            print(f"[ERROR] 유효한 텍스트가 없습니다!")
            return

        # 벡터라이저 초기화가 필요한 경우 처리
        if self.vectorizer is None or not hasattr(self.vectorizer, "vocabulary_"):
            print("[WARNING] 벡터라이저가 초기화되지 않아 새로 학습합니다.")
            self.vectorizer = CountVectorizer()
            X = self.vectorizer.fit_transform(filtered_texts)  # 학습 및 변환
        else:
            print("[INFO] 사전 훈련된 벡터라이저를 사용하여 변환 중...")
            X = self.vectorizer.transform(filtered_texts)  # 기존 벡터라이저 사용

        print(f"[INFO] 변환된 데이터 형태: {X.shape}")
        y = labels
        model = MultinomialNB()
        model.fit(X, y)
        print("[INFO] 모델 학습 완료")

        self.models[model_filename] = model
        self.save_model(model, model_filename)

    def save_model(self, model, model_filename):
        """모델을 pickle 파일로 저장"""
        model_path = os.path.join(self.model_folder, model_filename)
        with open(model_path, "wb") as model_file:
            pickle.dump((model, self.vectorizer), model_file)
        print(f"[INFO] 모델 저장 완료: {model_path}")

    def train_synonyms_model(self):
        """유사어 데이터 모델 학습"""
        synonyms_data = self.load_data(self.data_folders["synonyms"])
        if not synonyms_data:
            print("[WARNING] 유사어 데이터가 비어있습니다!")
            return
        self.train_model(synonyms_data, "synonyms_model.pkl")

    def train_order_model(self):
        """주문 데이터 모델 학습"""
        order_data = self.load_data(self.data_folders["order"])
        if not order_data:
            print("[WARNING] 주문 데이터가 비어있습니다!")
            return
        self.train_model(order_data, "order_model.pkl")

    def train_menu_quantity_model(self):
        """메뉴와 수량 데이터 모델 학습"""
        menu_quantity_data = self.load_data(self.data_folders["menu_quantity"])
        if not menu_quantity_data:
            print("[WARNING] 메뉴 수량 데이터가 비어있습니다!")
            return
        self.train_model(menu_quantity_data, "menu_quantity_model.pkl")


# 실행 코드
data_folders = {
    "synonyms": "AI/synonyms.json",
    "order": "AI/order_training_data.json",
    "menu_quantity": "AI/menu_quantity_training_data.json",
}

trainer = CustomModelTrainer(data_folders)
trainer.train_synonyms_model()
trainer.train_order_model()
trainer.train_menu_quantity_model()
