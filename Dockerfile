FROM python AS dev

WORKDIR /app

ADD requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt


FROM dev AS testing

RUN --mount=type=cache,target=/root/.cache/pip pip install pytest coverage

FROM dev AS prod

WORKDIR /var/www/efva

COPY app.py spiellogik.py wsgi.py login.py ./
COPY Datenbankverbindung/ ./Datenbankverbindung/
COPY static/ ./static/
COPY templates/ ./templates/

RUN openssl genrsa -des3 -out server.key 1024 && \
    openssl req -new -key server.key -out server.csr && \
    cp server.key server.key.org && \
    openssl rsa -in server.key.org -out server.key && \
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt && \
    openssl genrsa -des3 -out ca.key 4096 && \
    openssl req -new -x509 -days 365 -key ca.key -out ca.crt && \
    openssl genrsa -des3 -out client.key 1024 && \
    openssl req -new -key client.key -out client.csr && \
    openssl x509 -req -days 365 -in client.csr -CA ca.crt -CAkey ca.key -set_serial 01 -out client.crt


RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt update && \
    apt install apache2 apache2-dev -y

RUN --mount=type=cache,target=/root/.cache/pip pip install mod-wsgi