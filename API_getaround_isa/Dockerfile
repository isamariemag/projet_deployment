# image Python 
FROM python:3.9-slim

# répertoire de travail
WORKDIR /app

# dépendances
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app

# port 8000
EXPOSE 8000

# application avec le port fourni par Heroku
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]

