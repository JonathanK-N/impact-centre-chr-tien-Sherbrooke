FROM python:3.11

WORKDIR /app

COPY backend/ .

EXPOSE 8000

CMD ["python", "simple_server.py"]