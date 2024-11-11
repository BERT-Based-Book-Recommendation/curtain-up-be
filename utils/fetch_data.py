import pandas as pd
import os

# 데이터 불러오기
def load_vec_data(root="data/"):
  musical_vec_data_path = os.path.join(root, "musical_intro_vec.csv")
  # 파일 경로 존재 여부 확인
  if not os.path.exists(musical_vec_data_path):
      print(f"Error: {musical_vec_data_path} 파일을 찾을 수 없습니다.")
      return
  df = pd.read_csv(musical_vec_data_path)
  embedding_df = df.loc[:, '0':'767']
  
  return embedding_df, df.index


def load_data(root="data/"):
  musical_data_path = os.path.join(root, "musical_intro.csv")
  # 파일 경로 존재 여부 확인
  if not os.path.exists(musical_data_path):
      print(f"Error: {musical_data_path} 파일을 찾을 수 없습니다.")
      return
  df = pd.read_csv(musical_data_path)
  
  return df