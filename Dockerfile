# Python 베이스 이미지 선택
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치 (venv 및 빌드 도구)
RUN apt-get update && apt-get install -y python3-venv python3-dev build-essential

# 종속성 파일을 컨테이너로 복사
COPY requirements.txt /app/

# Python 가상환경 생성 및 패키지 설치
RUN python3 -m venv /app/swprojectenv && \
    /app/swprojectenv/bin/pip install --upgrade pip && \
    /app/swprojectenv/bin/pip install -r requirements.txt

# 디버깅: 가상환경의 실행 파일 확인
RUN ls -l /app/swprojectenv/bin/

# 애플리케이션 코드 복사
COPY . /app

# 기본 실행 명령
CMD ["/app/swprojectenv/bin/python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
