



import redis
from celery import Celery

broker = 'redis://127.0.0.1:6379'
backend = 'redis://127.0.0.1:6379/0'

app = Celery('tasks', broker=broker, backend=backend)
app.config_from_object('celeryconfig')

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)