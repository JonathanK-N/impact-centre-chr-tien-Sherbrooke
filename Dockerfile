# Dockerfile ultra-simple - une seule étape
FROM python:3.11

WORKDIR /app

# Installer Node.js dans l'image Python
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs

# Backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt gunicorn

# Frontend - build local puis copie
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Retour au backend
WORKDIR /app
COPY backend/ .
RUN cp -r frontend/dist/* app/static/frontend/ 2>/dev/null || mkdir -p app/static/frontend

# Init DB et démarrage
RUN python init_db.py
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]