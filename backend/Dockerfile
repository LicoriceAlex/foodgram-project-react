FROM python:3.7-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get upgrade -y && \
    pip install --upgrade pip && \
    pip3 install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ] 
