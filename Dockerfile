FROM python:3.11-alpine

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install -r requirements.txt

COPY backend/ .

RUN python init_db.py

EXPOSE 8000

CMD ["python", "-c", "from app import create_app; app = create_app(); app.run(host='0.0.0.0', port=8000)"]