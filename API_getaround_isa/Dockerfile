# Utiliser l'image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application, y compris le fichier modèle
COPY . /app

# Exposer le port 8000
EXPOSE 8000

# Commande pour lancer l'application avec le port fourni par Heroku
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]

