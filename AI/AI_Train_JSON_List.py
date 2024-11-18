import json
import os
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder

class MenuModelTrainer:
    def __init__(self, json_file, model_folder="model_folder", model_filename="menu_classifier.pkl"):
        self.json_file = json_file
        self.model_folder = model_folder
        self.model_filename = model_filename
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.is_fitted = False
        self.synonyms_data = {}  # 유사어 데이터 저장용

        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

    def load_data_from_json(self):
        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"JSON 파일 로드 오류: {e}")
            return [], []

        texts = []
        quantities = []

        for item in data:
            text = item["input"]
            quantity = item["output"]["quantity"]  # JSON 구조에 맞게 접근
            texts.append(text)
            quantities.append(quantity)

        # 수량 레이블 숫자 변환을 위한 LabelEncoder
        quantity_encoder = LabelEncoder()
        quantity_encoder.fit(quantities)

        return texts, quantities, quantity_encoder

    def train_model(self):
        print("데이터 로드 및 학습 시작...")
        texts, quantities, quantity_encoder = self.load_data_from_json()

        if not texts:
            print("학습할 데이터가 없습니다.")
            return

        X = self.vectorizer.fit_transform(texts)
        y = quantity_encoder.transform(quantities)  # 수량을 숫자 레이블로 변환

        self.model.fit(X, y)
        self.is_fitted = True
        self.save_model()
        print("모델 학습 완료 및 저장.")

    def save_model(self):
        model_path = os.path.join(self.model_folder, self.model_filename)
        try:
            with open(model_path, "wb") as model_file:
                pickle.dump((self.model, self.vectorizer, self.synonyms_data), model_file)
            print(f"모델 저장 완료: {model_path}")
        except IOError as e:
            print(f"모델 저장 오류: {e}")

    def load_model(self):
        model_path = os.path.join(self.model_folder, self.model_filename)
        try:
            with open(model_path, "rb") as model_file:
                self.model, self.vectorizer, self.synonyms_data = pickle.load(model_file)
            self.is_fitted = True
            print(f"모델 로드 완료: {model_path}")
        except (FileNotFoundError, pickle.PickleError) as e:
            print(f"모델 로드 오류: {e}")

# 실행 코드
if __name__ == "__main__":
    trainer = MenuModelTrainer(json_file="c:/order_training_data.json", model_folder=r"model")
    trainer.train_model()
