# Dockerfile ultra-simple - backend seulement
FROM python:3.11-slim

WORKDIR /app

# Backend
COPY backend/requirements.txt .
RUN pip install -r requirements.txt gunicorn

COPY backend/ .

# Frontend pré-buildé (copie locale)
RUN mkdir -p ./app/static/frontend
COPY frontend/dist/ ./app/static/frontend/

# Init DB et démarrage
RUN python init_db.py

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]