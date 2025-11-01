FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY backend/ .

EXPOSE 8000

CMD ["python3", "-c", "import http.server; import socketserver; PORT=8000; Handler=http.server.SimpleHTTPRequestHandler; httpd=socketserver.TCPServer(('', PORT), Handler); print(f'Server on {PORT}'); httpd.serve_forever()"]