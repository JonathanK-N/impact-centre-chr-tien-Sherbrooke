# Dockerfile ultra-simple - backend avec frontend intégré
FROM python:3.11-slim

WORKDIR /app

# Backend avec frontend déjà intégré
COPY backend/requirements.txt .
RUN pip install -r requirements.txt gunicorn

COPY backend/ .

# Init DB et démarrage
RUN python init_db.py

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]