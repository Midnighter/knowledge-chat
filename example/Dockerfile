FROM python:3.12-slim

WORKDIR /opt/chat

RUN apt-get update \
    && apt-get install --yes --no-install-recommends \
        ca-certificates \
        openssl \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt ./

RUN pip install --no-cache-dir --no-deps --requirement requirements.txt

WORKDIR /opt/chat/dist

COPY ./dist ./

WORKDIR /opt/chat

RUN pip install --no-cache-dir --no-deps dist/knowledge_chat*.whl

COPY ./app .

EXPOSE 8000

CMD ["chainlit", "run", "--headless", "--host", "0.0.0.0", "app.py"]
