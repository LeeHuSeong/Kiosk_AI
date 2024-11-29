import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer  # 추가: 벡터라이저 타입 검증

def load_model_and_vectorizer(model_path):
    """
    모델과 벡터라이저를 로드하고 정보를 출력하는 함수.

    Args:
        model_path (str): 모델 파일 경로.

    Returns:
        model: 로드된 모델 객체.
        vectorizer: 로드된 벡터라이저 객체.
    """
    try:
        with open(model_path, "rb") as model_file:
            model, vectorizer = pickle.load(model_file)

        # 벡터라이저 검증
        if not isinstance(vectorizer, CountVectorizer):
            print("로드된 벡터라이저가 CountVectorizer 형식이 아닙니다.")
            return None, None

        print("모델과 벡터라이저를 성공적으로 로드했습니다.")
        return model, vectorizer

    except FileNotFoundError:
        print(f"파일을 찾을 수 없습니다: {model_path}")
        return None, None
    except Exception as e:
        print(f"모델 로드 중 오류 발생: {e}")
        return None, None


def print_model_info(model, vectorizer):
    """
    모델과 벡터라이저의 기본 정보를 출력하는 함수.

    Args:
        model: 로드된 머신러닝 모델.
        vectorizer: 로드된 TfidfVectorizer.
    """
    if model:
        print("\n[모델 정보]")
        print(f"모델 클래스: {model.__class__.__name__}")

    if vectorizer:
        print("\n[벡터라이저 정보]")
        print(f"벡터 크기 (단어 수): {len(vectorizer.vocabulary_)}")
        if len(vectorizer.vocabulary_) > 0:
            print(f"단어 목록 (일부): {list(vectorizer.vocabulary_.keys())[:10]}")
        else:
            print("벡터라이저에 단어가 없습니다.")


if __name__ == "__main__":
    # 모델 파일 경로 지정
    model_folder = "model"  # 모델 저장 폴더
    model_filename = "menu_order.pkl"  # 저장된 모델 파일명
    model_path = os.path.join(model_folder, model_filename)

    # 모델과 벡터라이저 로드
    model, vectorizer = load_model_and_vectorizer(model_path)

    # 모델과 벡터라이저 정보 출력
    if model and vectorizer:
        print_model_info(model, vectorizer)
