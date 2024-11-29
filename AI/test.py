import json
import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class MenuModelTrainer:
    def __init__(self, json_file, model_folder="model_folder", model_filename="menu_synonyms.pkl"):
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
            return [], []

        texts = []
        labels = []

        # 유사어 사전을 처리하여 텍스트와 라벨 생성
        for label, synonyms in data.items():
            for group in synonyms:
                if isinstance(group, list):
                    for synonym in group:
                        texts.append(synonym)
                        labels.append(label)
                else:
                    texts.append(group)
                    labels.append(label)

        return texts, labels

    def train_model(self):
        print("데이터 로드 및 학습 시작...")
        texts, labels = self.load_data_from_json()

        if not texts:
            print("학습할 데이터가 없습니다.")
            return

        # 텍스트 데이터를 벡터화하여 학습
        X = self.vectorizer.fit_transform(texts)
        y = labels

        try:
            self.model.fit(X, y)
            self.is_fitted = True
            self.save_model()
            print("모델 학습 완료 및 저장.")
        except Exception as e:
            print(f"모델 학습 중 오류 발생: {e}")

    def save_model(self):
        model_path = os.path.join(self.model_folder, self.model_filename)
        try:
            with open(model_path, "wb") as model_file:
                pickle.dump((self.model, self.vectorizer), model_file)
            print(f"모델 저장 완료: {model_path}")
        except IOError as e:
            print(f"모델 저장 오류: {e}")

    def load_model(self):
        model_path = os.path.join(self.model_folder, self.model_filename)
        try:
            with open(model_path, "rb") as model_file:
                self.model, self.vectorizer = pickle.load(model_file)
            self.is_fitted = True
            print(f"모델 로드 완료: {model_path}")
        except (FileNotFoundError, pickle.PickleError) as e:
            print(f"모델 로드 오류: {e}")


# 실행 코드
if __name__ == "__main__":
    trainer = MenuModelTrainer(json_file="AI/synonyms.json", model_folder="model")
    trainer.train_model()
