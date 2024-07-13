FROM python

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/requirements.txt