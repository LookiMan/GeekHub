
# Upgrade pip:

`python -m pip install --upgrade pip`

# Install requirements:

`python -m pip install -r requirements.txt`

# Celery

https://django.fun/docs/celery/ru/5.1/userguide/configuration/#std-setting-worker_max_tasks_per_child


`celery -A config.celery worker -Q celery -l INFO --concurrency 1`


If an error occurs:


`Use the {_TO_NEW_KEY[setting]} instead') in version 6.0.0 appear.`


Run this command:


`celery upgrade settings path/to/settings.py`


this automatically update the following to:


```
CELERY_ACCEPT_CONTENT = ['**']
CELERY_BROKER_URL = "**"
CELERY_TIMEZONE = "**"
CELERY_RESULT_BACKEND = "**"
```

to this:

```
accept_content = ['**']
CELERY_broker_url = "**"
timezone = "**"
result_backend = "**"
```

# Project root:

`GeekHub/FinalProject`

# Activate virtual environment:

`../../Scripts/Activate.ps1`

# Run Ngrok:

`cd "dev"`

`./ngrok.exe http 127.0.0.1:8000`

# Run webserver:

`daphne -b 0.0.0.0 -p 8000 config.asgi:application`

# Run sass:

`cd chat/static/assets`

`sass --watch scss:css`