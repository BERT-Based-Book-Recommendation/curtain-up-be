from fastapi import APIRouter
from utils.model import load_model
from utils.calc import load_data, remove_stopwords, create_similarity_df, show_recommend_list
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer
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
  books, reviews = load_data()
  # 모델 로드
  model = load_model()
  # 불용어 처리
  filtered_input = remove_stopwords(inputText)
  # 임베딩 벡터 구하기
  input_vec = model.encode([filtered_input])
  book_vec = model.encode(books['Introduction'])
  rv_vec = model.encode(reviews['Review'])
  # 코사인 유사도 계산
  book_similars = cosine_similarity(input_vec,book_vec)
  rv_similars = cosine_similarity(input_vec,rv_vec)
  # 유사도 값을 float으로 변환
  book_similars = book_similars.astype(float)
  rv_similars = rv_similars.astype(float)
  # 유사도 계산 값 df로 변환
  book_s_df, rv_s_df = create_similarity_df(books, reviews, book_similars, rv_similars)

  # 추천 스코어 계산
  book_star = books[['Num', 'Review']]
  final_df = reduce(lambda x, y: pd.merge(x, y, how='inner', on='Num'),[book_s_df, rv_s_df, book_star])
  final_df['total'] = 0.5*(((0.5 * final_df['similars_book']) + (0.5 *final_df['similars_rv']))) + 0.5*(final_df['Review']/10.0)

  # 추천 스코어가 높은 4개의 book
  recommend_list = final_df.sort_values(by='total', ascending=False)[:4]['Num'].to_list()
  result = show_recommend_list(books, recommend_list)

  # 출력 결과를 JSON 형식으로 반환
  return result

