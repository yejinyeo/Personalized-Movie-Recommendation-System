FROM python:3.12-slim-bookworm

WORKDIR /app

# 필요한 빌드 도구 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cython3 \
    && rm -rf /var/lib/apt/lists/*

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
