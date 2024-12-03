from fastapi import APIRouter
from pydantic import BaseModel
from utils.model import load_model
from utils.fetch_data import load_vec_data, load_musical_data, load_reveiw_data
from utils.process import remove_stopwords
from fastapi.responses import JSONResponse
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

router = APIRouter()

# 요청 데이터 모델 정의
class RecommendRequest(BaseModel):
    inputText: str

@router.get("/")
async def root():
    return {"Hello": "World"}

@router.post("/model", response_class=JSONResponse)
async def recommend_book(request: RecommendRequest):
    inputText = request.inputText  # 요청 본문에서 inputText 가져오기

    # 데이터 로드
    musical = load_musical_data()
    review = load_reveiw_data()
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
    top_2_indices = book_similars.argsort()[-2:][::-1]  
    
    # 상위 2개의 책의 name, pre_intro 및 유사도 정보 추출
    top_books = []
    for idx in top_2_indices:
        book_index = book_indices[idx]
        most_similar_book = musical.loc[book_index, ['name', 'image', 'pre_intro']]
        # review 데이터 프레임에서 key가 most_similar_book['name']인 행의 내용을 가져오기
        related_reviews = review[review['key'] == most_similar_book['name']][['rv_title', 'writer']]
        
        # rv_title과 writer를 객체로 묶어 리스트로 변환
        reviews_list = related_reviews.apply(
            lambda row: {"rv_title": row['rv_title'], "writer": row['writer']}, axis=1
        ).tolist()
        
        top_books.append({
            "name": most_similar_book['name'],
            "image": most_similar_book['image'],
            "pre_intro": most_similar_book['pre_intro'],
            "similarity": book_similars[idx],
            "review": reviews_list
        })

    # 출력 결과를 JSON 형식으로 반환
    return JSONResponse(content={"recommended_books": top_books})
