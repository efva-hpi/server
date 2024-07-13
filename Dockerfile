FROM python

WORKDIR /app

COPY app.py spiellogik.py requirements.txt /app/
COPY Datenbankverbindung/ /app/Datenbankverbindung/
COPY static/ /app/static/
COPY templates/ /app/templates/

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt

ENTRYPOINT ["flask", "run", "--debug", "-p 3000", "--host=0.0.0.0"]