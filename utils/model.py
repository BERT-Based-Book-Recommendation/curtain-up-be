import torch
import os
import sys
sys.path.append("..")

# 모델 불러오기
def load_model(root="model/"):
    model_path = os.path.join(root, "book_intro_train_fixlib_batch8_softmax_BERT.pt")
    # 전체 모델을 불러오는 경우
    model = torch.load(model_path, map_location=torch.device('cpu'))
    # 평가 모드로 전환
    model.eval()
    return model

