from os import path

base = path.realpath(path.join(path.dirname(__file__), '..', '..', '..'))
pidfile = path.join(base, 'pids', 'gunicorn.pid')
errorlog = path.join(base, 'log', 'gunicorn.error.log')

workers = 2

user = 'www-data'
group = 'www-data'
bind = '127.0.0.1:8001'
accesslog = None
loglevel = 'info'
