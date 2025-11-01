# -----------------------------------------------------------------------------
# Étape 1 : compilation du frontend React avec Vite
# -----------------------------------------------------------------------------
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN chmod -R +x node_modules/.bin || true
RUN ./node_modules/.bin/vite build

# -----------------------------------------------------------------------------
# Étape 2 : image backend Flask + bundle frontend
# -----------------------------------------------------------------------------
FROM python:3.11-slim AS backend

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app \
    PORT=8000

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .
COPY --from=frontend-builder /app/frontend/dist ./app/static/frontend

EXPOSE 8000

CMD ["sh", "-c", "gunicorn app:create_app --bind 0.0.0.0:${PORT:-8000}"]

