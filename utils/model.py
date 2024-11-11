import os
import sys
sys.path.append("..")
from sentence_transformers import SentenceTransformer

# 모델 불러오기
def load_model(root="model/epoch_8/39"):
    # 정확한 모델 경로 설정
    model_path = os.path.join(root)
    
    # 모델 로드
    model = SentenceTransformer(model_path, trust_remote_code=True)

    # 평가 모드로 전환
    model.eval()
    return model