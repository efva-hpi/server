FROM python AS dev

WORKDIR /app

ADD requirements.txt ./

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt


FROM dev AS testing

RUN --mount=type=cache,target=/root/.cache/pip pip install pytest coverage

FROM dev AS prod

WORKDIR /var/www/efva

COPY app.py spiellogik.py wsgi.py login.py uwsgi.ini ./
COPY Datenbankverbindung/ ./Datenbankverbindung/
COPY static/ ./static/
COPY templates/ ./templates/

RUN --mount=type=cache,target=/root/.cache/pip pip install uwsgi
