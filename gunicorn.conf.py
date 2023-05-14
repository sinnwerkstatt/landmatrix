bind = "unix:../run/gunicorn.socket"
pidfile = "../run/gunicorn.pid"

wsgi_app = "config.wsgi"

limit_request_line = 0
timeout = 360

workers = 4
threads = 4
