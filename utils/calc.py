import pandas as pd
import os

# 데이터 불러오기
def load_data(root="data/"):
  bookdata_path = os.path.join(root, "book.csv")
  reviewdata_path = os.path.join(root, "review.csv")
  # 파일 경로 존재 여부 확인
  if not os.path.exists(bookdata_path):
      print(f"Error: {bookdata_path} 파일을 찾을 수 없습니다.")
      return
  if not os.path.exists(reviewdata_path):
      print(f"Error: {reviewdata_path} 파일을 찾을 수 없습니다.")
      return
  book_df = pd.read_csv(bookdata_path)
  review_df = pd.read_csv(reviewdata_path)
  return book_df, review_df

# 불용어 처리
def remove_stopwords(input):
  stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', '해줘', '소설', '이야기', '해', '추천해줘', '소설을', '소설이', '이야기를', '이야기가']
  filtered_input = ' '.join([word for word in input.split() if not word in stopwords])
  return filtered_input

# 유사도 계산 값 df로 변환
def create_similarity_df(books, reviews, book_similars, rv_similars):
  book_s_df = pd.DataFrame({
      'Num': books['Num'],  # 책 ID
      'similars_book': book_similars[0]  # 유사도 값 (1차원 배열)
  })
  rv_s_df = pd.DataFrame({
      'Num': reviews['Num'],  # 리뷰 ID
      'similars_rv': rv_similars[0]  # 유사도 값 (1차원 배열)
  })
  rv_s_df = rv_s_df.groupby('Num').mean().reset_index()
  
  return book_s_df, rv_s_df

# 도서 제목과 소개 출력
def show_recommend_list(books, recommend_list):
  filtered_books = books[books['Num'].isin(recommend_list)]
  filtered_books = filtered_books.drop_duplicates(subset='Num').reset_index(drop=True)
  result_df = filtered_books[['Introduction', 'Title']]

  return result_df