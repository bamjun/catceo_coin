# Python 3.12.3 이미지를 기반으로 생성
FROM python:3.12.3-slim

# 작업 디렉토리 설정
WORKDIR /app

# Poetry 설치
RUN pip install poetry

# Poetry 환경 변수 설정 (가상환경을 시스템 python 사용으로 설정)
ENV POETRY_VIRTUALENVS_CREATE=false

# Poetry 설치 파일 복사 및 종속성 설치
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev

# 앱 코드 복사
COPY . .

# 환경 변수 설정
ENV DJANGO_SETTINGS_MODULE=config.settings

# Django와 Channels를 위한 명령어 실행
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8001 config.asgi:application"]
