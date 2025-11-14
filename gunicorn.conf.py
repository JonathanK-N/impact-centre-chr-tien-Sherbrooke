import os

bind = f"0.0.0.0:{os.environ.get('PORT', 8000)}"
workers = 1
timeout = 300
keepalive = 2
max_requests = 1000
max_requests_jitter = 100
preload_app = True