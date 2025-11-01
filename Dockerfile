FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production

CMD python init_app.py && gunicorn --bind 0.0.0.0:$PORT --workers 1 app:app