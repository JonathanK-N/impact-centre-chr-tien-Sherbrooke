FROM python:3.11-alpine

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

# Debug: vérifier la structure
RUN find . -name "frontend" -type d
RUN ls -la ./app/static/frontend/ || echo "Dossier frontend non trouvé"
RUN ls -la ./app/static/frontend/index.html || echo "index.html non trouvé"

RUN python init_db.py

EXPOSE 8000

CMD ["python", "-c", "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=8000)"]