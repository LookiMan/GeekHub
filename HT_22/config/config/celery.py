import os
import sys

from celery import Celery

# Set the default Django settings module for the 'celery' program.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


celery_app = Celery('config', broker="amqp://guest@localhost/", backend='amqp', fixups=[])
celery_app.config_from_object('config.settings', namespace='CELERY')
celery_app.autodiscover_tasks()