# Upgrade pip:

`python -m pip install --upgrade pip`

# Install requirements:

`python -m pip install -r requirements.txt`


# Project root:

`GeekHub/FinalProject`

# Activate virtual environment:

`../../Scripts/Activate.ps1`

# Run Ngrok:

`cd "dev"`

`./ngrok.exe http 127.0.0.1:8000`

# Run webserver:

`daphne -b 127.0.0.1 -p 8000 config.asgi:application`

# Run sass:

`cd chat/static/assets`

`sass --watch scss\style.scss:css\style.css`
