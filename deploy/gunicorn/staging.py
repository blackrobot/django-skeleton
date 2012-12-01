from os import path

base = path.realpath(path.join(path.dirname(__file__), "../../../"))
pidfile = path.join(base, "pids/gunicorn.pid")
errorlog = path.join(base, "log/gunicorn.error.log")

user = "www-data"
group = "www-data"
bind = "127.0.0.1:9001"
accesslog = None
loglevel = "info"

workers = 2
