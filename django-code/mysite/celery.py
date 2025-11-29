import os
from celery import Celery
from pathlib import Path
from dotenv import load_dotenv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

app = Celery('mysite')

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, ".celery.env"))

class CelerySettings:
    broker_port=os.environ['BROKER_PORT']
    broker_url=os.environ['BROKER_URL']
    result_backend=os.environ['RESULT_BACKEND']
    accept_content=[os.environ['ACCEPT_CONTENT']]
    task_serializer=os.environ['TASK_SERIALIZER']
    result_serializer=os.environ['RESULT_SERIALIZER']
    timezone=os.environ['TIMEZONE']
    worker_concurrency=int(os.environ['WORKER_CONCURRENCY'])

app.config_from_object(CelerySettings)
app.autodiscover_tasks()