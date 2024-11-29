import os
import pickle
import re
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

class DialectModelTrainer:
    def __init__(self, data_folder, model_folder="model"):
        self.data_folder = data_folder
        self.model_folder = model_folder
        self.vectorizer = None
        self.model = None

        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

    def load_data(self):
        """ 데이터를 JSON 형식으로 로드 """
        data = {}
        total_files = sum([len(files) for _, _, files in os.walk(self.data_folder) if files])  # 전체 파일 수
        processed_files = 0  # 처리한 파일 수

        # data_folder 내 모든 서브 폴더와 파일 순회
        for root, dirs, files in os.walk(self.data_folder):
            for file in files:
                if file.endswith(".json"):  # JSON 파일만 처리
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            file_data = json.load(f)
                            # 파일에서 로드한 데이터가 존재하면 처리
                            if file_data:
                                for key, values in file_data.items():
                                    if key not in data:
                                        data[key] = []
                                    data[key].extend(values)
                        processed_files += 1
                        print(f"진행 상태: {processed_files}/{total_files} 파일 처리 중...")
                    except json.JSONDecodeError as e:
                        print(f"JSONDecodeError: {file_path} 파일을 읽는 중 오류 발생: {e}")

        if not data:
            print("경고: 로드된 데이터가 없습니다.")
        else:
            print(f"총 {len(data)}개의 데이터 항목이 로드되었습니다.")  # 데이터가 제대로 로드되었는지 확인
        return data

    def clean_text(self, text):
        """ 텍스트를 정제하는 함수: 소문자화, 불필요한 특수문자만 제거 """
        text = text.lower()  # 소문자화
        text = re.sub(r'[^\w\s\d가-힣]', '', text)  # 알파벳, 숫자, 공백만 남기기 (특수문자만 제거)
        return text.strip()

    def train_model(self, data):
        """ 주어진 데이터를 바탕으로 모델 학습 """
        texts = []
        labels = []

        for key, values in data.items():
            for value_set in values:
                texts.append(" ".join(value_set))  # 여러 값을 공백으로 구분한 텍스트로 변환
                labels.append(key)  # 키는 레이블로 사용

        # 빈 텍스트 필터링 및 정제
        filtered_texts = [self.clean_text(text) for text in texts if text.strip() != ""]

        if len(filtered_texts) == 0:
            print("에러: 유효한 텍스트가 없습니다!")
            return

        # CountVectorizer로 텍스트 벡터화
        self.vectorizer = CountVectorizer()
        X = self.vectorizer.fit_transform(filtered_texts)
        y = labels

        print(f"학습된 벡터 크기: {X.shape}")  # 벡터화 후 벡터 크기 확인

        self.model = MultinomialNB()
        self.model.fit(X, y)

    def save_model(self):
        """ 모델과 벡터라이저 저장 """
        try:
            model_filename = "dialect_model.pkl"
            model_path = os.path.join(self.model_folder, model_filename)

            # 모델과 벡터라이저를 함께 저장
            with open(model_path, "wb") as model_file:
                pickle.dump((self.model, self.vectorizer), model_file)

            # 벡터라이저만 별도로 저장
            vectorizer_filename = "vectorizer.pkl"
            vectorizer_path = os.path.join(self.model_folder, vectorizer_filename)
            with open(vectorizer_path, "wb") as vectorizer_file:
                pickle.dump(self.vectorizer, vectorizer_file)

            print(f"모델과 벡터라이저 저장 완료: {model_path}, {vectorizer_path}")
        except Exception as e:
            print(f"모델 저장 도중 오류 발생: {e}")

data_folder = "D:/unzipped_data"  # 데이터 폴더 경로
trainer = DialectModelTrainer(data_folder)
data = trainer.load_data()  # 데이터 로드
if data:
    trainer.train_model(data)  # 모델 학습
    trainer.save_model()  # 모델 저장
