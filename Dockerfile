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

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean && \
    apt update && \
    apt install apache2 apache2-dev -y

RUN --mount=type=cache,target=/root/.cache/pip pip install mod-wsgi

RUN mod_wsgi-express setup-server wsgi.py https-port 3000 https-only --server-name efva.konsti.store --user www-data --group www-data --server-root /etc/mod_wsgi-express-3000