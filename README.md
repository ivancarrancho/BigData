# BigData
Data processing of sales vs weather


## Run:
    docker-compose build backend

## Run:
    docker-compose up backend

## Enter to bash:
    docker-compose exec backend bash

## Enter to console to rocks inside:
    ipython

# If you are scared

## Stop all containers:
    docker stop $(docker ps -a -q)

## Remove all temporary containers:
    docker rm $(docker ps -a -q)