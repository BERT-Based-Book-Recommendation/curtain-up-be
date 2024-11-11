from fastapi import APIRouter
from utils.model import load_model
from utils.fetch_data import load_vec_data, load_data
from utils.process import remove_stopwords
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from functools import reduce

router = APIRouter()

@router.get("/")
async def root():
    return {"Hello": "World"}

@router.post("/model", response_class=JSONResponse)
async def recommend_book(inputText: str):
  # 데이터 로드
  musical_intro = load_data()
  # 모델 로드
  model = load_model()
  # 불용어 처리
  filtered_input = remove_stopwords(inputText)
  # 임베딩 벡터 구하기
  input_vec = model.encode([filtered_input])
  books_vec, book_indices = load_vec_data()

  # 코사인 유사도 계산
  book_similars = cosine_similarity(input_vec, books_vec)[0]
  
  # 유사도가 가장 높은 상위 4개의 책 인덱스 선택 및 유사도 순으로 정렬
  top_4_indices = book_similars.argsort()[-4:][::-1]
  
  # 상위 4개의 책의 name, pre_intro 및 유사도 정보 추출
  top_books = []
  for idx in top_4_indices:
      book_index = book_indices[idx]
      most_similar_book = musical_intro.loc[book_index, ['name', 'pre_intro']]
      top_books.append({
          "name": most_similar_book['name'],
          "pre_intro": most_similar_book['pre_intro'],
          "similarity": book_similars[idx]
      })
  
  # 출력 결과를 JSON 형식으로 반환
  return JSONResponse(content={"recommended_books": top_books})