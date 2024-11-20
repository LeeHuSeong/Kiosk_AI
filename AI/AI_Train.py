import os
import zipfile
import numpy as np
import pickle
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer

class MenuModelTrainer:
    def __init__(self, data_folder, unzipped_folder="unzipped_data", model_folder="model_folder", model_filename="menu_classifier.pkl"):
        self.data_folder = data_folder
        self.unzipped_folder = unzipped_folder
        self.model_folder = model_folder
        self.model_filename = model_filename
        self.vectorizer = CountVectorizer()
        self.model = MultinomialNB()
        self.is_fitted = False  # 모델 및 벡터라이저가 처음 학습되었는지 여부를 나타내는 플래그

        # 모델 폴더가 존재하지 않으면 생성
        if not os.path.exists(self.model_folder):
            os.makedirs(self.model_folder)

    def unzip_data(self):
        try:
            print("압축 파일 풀기 시작...")
            if not os.path.exists(self.unzipped_folder):
                os.makedirs(self.unzipped_folder)

            zip_count = 0
            for root, dirs, files in os.walk(self.data_folder):
                for filename in files:
                    if filename.endswith(".zip"):
                        zip_path = os.path.join(root, filename)
                        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                            extract_path = os.path.join(self.unzipped_folder, filename.replace(".zip", ""))
                            if not os.path.exists(extract_path):
                                os.makedirs(extract_path)
                            zip_ref.extractall(extract_path)
                        zip_count += 1
                        print(f"{zip_path} 압축 해제 완료.")

            if zip_count == 0:
                print("압축 파일이 발견되지 않았습니다.")
            else:
                print(f"{zip_count}개의 압축 파일을 해제했습니다.")
        except Exception as e:
            print(f"압축 해제 도중 오류 발생: {e}")

    def load_data_and_train_incrementally(self):
        print("데이터 로드 및 점진적 학습 시작...")
        batch_num = 0

        # 압축 해제한 폴더와 원본 데이터 폴더 모두에서 학습
        folders_to_process = [self.unzipped_folder, self.data_folder]

        try:
            for folder in folders_to_process:
                for root, dirs, files in os.walk(folder):
                    for filename in files:
                        if filename.endswith(".txt"):
                            file_path = os.path.join(root, filename)
                            with open(file_path, "r", encoding="utf-8") as file:
                                text = file.read().strip()
                                if text:
                                    X = self.vectorizer.fit_transform([text]) if not self.is_fitted else self.vectorizer.transform([text])
                                    y = [filename.split('_')[0]]  # 라벨 예시: 파일명에서 구분

                                    if not self.is_fitted:
                                        self.model.partial_fit(X, y, classes=np.unique(y))
                                        self.is_fitted = True
                                    else:
                                        self.model.partial_fit(X, y)

                batch_num += 1
                print(f"배치 {batch_num} 학습 완료 및 모델 저장됨.")
                self.save_model()

            print("데이터 로드 및 점진적 학습 완료.")
        except Exception as e:
            print(f"학습 도중 오류 발생: {e}")

    def save_model(self):
        try:
            model_path = os.path.join(self.model_folder, self.model_filename)
            with open(model_path, "wb") as model_file:
                pickle.dump((self.model, self.vectorizer), model_file)
            print(f"모델 저장 완료: {model_path}")
        except Exception as e:
            print(f"모델 저장 도중 오류 발생: {e}")

    def load_model(self):
        try:
            model_path = os.path.join(self.model_folder, self.model_filename)
            with open(model_path, "rb") as model_file:
                self.model, self.vectorizer = pickle.load(model_file)
            self.is_fitted = True
            print(f"모델 로드 완료: {model_path}")
        except Exception as e:
            print(f"모델 로드 도중 오류 발생: {e}")

    def train(self):
        self.unzip_data()  # 압축 파일 풀기
        self.load_data_and_train_incrementally()  # 데이터 불러와 점진적으로 학습하기

# 학습 실행 코드 (단독으로 실행될 경우)
if __name__ == "__main__":
    trainer = MenuModelTrainer(data_folder=r"D:/unzipped_data", unzipped_folder=r"D:\unzipped_data", model_folder=r"model")
    trainer.train()
    input("학습이 끝났습니다. Enter 키를 눌러 종료하세요.")