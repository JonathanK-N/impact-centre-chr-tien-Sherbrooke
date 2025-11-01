FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY index.html .

EXPOSE 8000

CMD ["python3", "-m", "http.server", "8000", "--bind", "0.0.0.0"]