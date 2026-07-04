FROM python:3.11-slim

WORKDIR /srv

COPY app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY wiki ./wiki
COPY app ./app

WORKDIR /srv/app
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "gunicorn --bind :$PORT --workers 2 --threads 4 app:app"]
