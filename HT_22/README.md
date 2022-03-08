## Install Erlang

## https://infoit.com.ua/linux/kak-ustanovit-erlang-na-ubuntu-20-04-lts/

`sudo apt update`

`sudo apt upgrade`

`echo "deb https://packages.erlang-solutions.com/ubuntu focal contrib" | sudo tee /etc/apt/sources.list.d/rabbitmq.list`

`sudo apt update`

`sudo apt install erlang`

## Test erlang

`erl`

## Install rabbitmq-server and its dependencies

## https://www.rabbitmq.com/install-debian.html#apt-cloudsmith

`sudo apt-get install rabbitmq-server -y --fix-missing`

## Start the Server

`systemctl start rabbitmq-server`

## To start and stop the server, use the systemctl tool. The service name is rabbitmq-server:

## stop the local node

`sudo systemctl stop rabbitmq-server`

## start it back

`sudo systemctl start rabbitmq-server`

systemctl status rabbitmq-server will report service status as observed by systemd (or similar service manager):

## check on service status as observed by service manager

`sudo systemctl status rabbitmq-server`

## Start celery instance

`celery -A config worker --loglevel=INFO`

`celery -A config.celery worker -Q celery,scraper -l INFO`
