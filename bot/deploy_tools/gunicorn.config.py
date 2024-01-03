import os
pythonpath = '/usr/src/app'
bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8000')
workers = os.environ.get('GUNICORN_WORKERS', 3)
