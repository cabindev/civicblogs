# Gunicorn configuration file
import os

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "8000")
backlog = 2048

# Worker processes
workers = int(os.environ.get("WEB_CONCURRENCY", "2"))
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 5000
max_requests_jitter = 500

# Logging
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'civicblogs'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None