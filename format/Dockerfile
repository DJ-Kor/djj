FROM python:3.9.17-slim-bookworm

RUN apt-get update && \
    apt-get install -y vim && \
    # cleanup
    rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /requirements.txt    

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir -p /www/app
WORKDIR /www/app

## consider cache
# ENV RAG_EMBEDDING_MODEL_DIR="www/app/cache/embedding/models"

# Hugging Face 모델 다운로드
VOLUME [ "huggingface-models", "/www/app/huggingface-models" ]
ARG MODELS="nomic-ai/nomic-embed-text-v1,BM-K/KoSimCSE-roberta-multitask,sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
COPY ./download_models.py /www/download_models.py




RUN python ../download_models.py "${MODELS}"

CMD uvicorn --host=0.0.0.0 --port 8000 main:app --reload --forwarded-allow-ips '*'
# CMD gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 --timeout 300 main:app
# CMD python gunicorn_runner.py          

FROM python:3.8.10    

RUN apt-get update && \ 
    apt-get install -y vim

RUN pip install --upgrade pip

RUN useradd --no-create-home -u 1018 nginx

ADD . /www
RUN chown nginx /www

RUN mkdir -p /www/gcp_result
RUN chown nginx /www/gcp_result

WORKDIR /www

COPY ./requirements.txt /www/requirements.txt
COPY ./app/ /www/app/

RUN ls -laR /www/app

RUN pip install -r /www/requirements.txt

WORKDIR /www/app

CMD uvicorn --host=0.0.0.0 --port 8000 main:app --reload
