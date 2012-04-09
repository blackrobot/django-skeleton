import os

home_dir = os.path.realpath(os.path.join(
    os.path.dirname(__file__), "../../../",
))

user = "deploy"
group = "deploy"
bind = "127.0.0.1:9000"
workers = 2
pidfile = "%s/pids/supervisord.pid" % home_dir
errorlog = "%s/logs/gunicorn.error.log" % home_dir
accesslog = None
loglevel = "info"
