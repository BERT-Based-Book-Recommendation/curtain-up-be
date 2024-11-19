# Python 베이스 이미지 선택
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일을 컨테이너로 복사
COPY requirements.txt /app/

# 가상환경에 필요한 패키지 설치
RUN python -m venv /app/swprojectenv && \
    /app/swprojectenv/bin/pip install --upgrade pip && \
    /app/swprojectenv/bin/pip install -r requirements.txt

# 가상환경의 파일 확인 (디버깅용)
RUN ls -l /app/swprojectenv/bin/

# 애플리케이션 코드 복사
COPY . /app

# 가상환경에서 uvicorn 절대 경로로 실행
CMD ["/app/swprojectenv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
