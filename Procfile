web: newrelic-admin run-program gunicorn creditswarm.wsgi -b 0.0.0.0:$PORT -k gevent
celeryd: newrelic-admin run-program python manage.py celeryd -E -B --loglevel=INFO
