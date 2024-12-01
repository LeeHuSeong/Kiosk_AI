import json
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import re


class MenuModelTrainer:
    def __init__(self, json_file, model_folder="model_folder", model_filename="menu_order.pkl"):
        self.json_file = json_file
        self.model_folder = model_folder
        self.model_filename = model_filename
        self.vectorizer = CountVectorizer(analyzer='word', tokenizer=None, stop_words=None)  # 기본 토큰화 사용
        self.model = MultinomialNB()
        self.is_fitted = False

        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

    def load_data_from_json(self):
        try:
            with open(self.json_file, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"JSON 파일 로드 오류: {e}")
            return [], [], []

        texts = []
        menus = []
        quantities = []

        # 새로운 데이터 형식에 맞춰 메뉴와 수량 추출
        for entry in data:
            if "input" in entry and "output" in entry:
                text = entry["input"]
                menu = entry["output"]["menu"]
                quantity = entry["output"]["quantity"]
                
                texts.append(text)
                menus.append(menu)
                quantities.append(quantity)

        return texts, menus, quantities

    def train_model(self):
        print("데이터 로드 및 학습 시작...")
        texts, menus, quantities = self.load_data_from_json()

        if not texts:
            print("학습할 데이터가 없습니다.")
            return

        # 텍스트 데이터를 벡터화하여 학습
        X = self.vectorizer.fit_transform(texts)
        y_menu = menus
        y_quantity = quantities

        try:
            # 메뉴 모델 학습
            self.menu_model = MultinomialNB()
            self.menu_model.fit(X, y_menu)
            
            # 수량 모델 학습
            self.quantity_model = MultinomialNB()
            self.quantity_model.fit(X, y_quantity)
            
            self.is_fitted = True
            self.save_model()
            print("모델 학습 완료 및 저장.")
        except Exception as e:
            print(f"모델 학습 중 오류 발생: {e}")

    def save_model(self):
        model_path = os.path.join(self.model_folder, self.model_filename)
        try:
            with open(model_path, "wb") as model_file:
                pickle.dump({
                    "menu_model": self.menu_model,
                    "quantity_model": self.quantity_model,
                    "vectorizer": self.vectorizer
                }, model_file)
            print(f"모델 저장 완료: {model_path}")
        except IOError as e:
            print(f"모델 저장 오류: {e}")

    def load_model(self):
        model_path = os.path.join(self.model_folder, self.model_filename)
        try:
            with open(model_path, "rb") as model_file:
                models = pickle.load(model_file)
                self.menu_model = models["menu_model"]
                self.quantity_model = models["quantity_model"]
                self.vectorizer = models["vectorizer"]
            self.is_fitted = True
            print(f"모델 로드 완료: {model_path}")
        except (FileNotFoundError, pickle.PickleError) as e:
            print(f"모델 로드 오류: {e}")

    def predict(self, input_text):
        if not self.is_fitted:
            print("모델이 학습되지 않았습니다.")
            return None

        # 입력 텍스트 벡터화
        X = self.vectorizer.transform([input_text])

        # 메뉴 예측
        predicted_menu = self.menu_model.predict(X)[0]

        # 수량 예측
        predicted_quantity = self.quantity_model.predict(X)[0]

        return {
            "menu": predicted_menu,
            "quantity": predicted_quantity
        }


# 실행 코드
if __name__ == "__main__":
    trainer = MenuModelTrainer(json_file="AI/order_training_data.json", model_folder="model")
    trainer.train_model()
