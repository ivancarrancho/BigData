FROM tiangolo/uwsgi-nginx-flask:python3.6

# Dependencies for Couchbase
RUN wget -O - http://packages.couchbase.com/ubuntu/couchbase.key | apt-key add -
RUN echo "deb http://packages.couchbase.com/ubuntu stretch stretch/main" > /etc/apt/sources.list.d/couchbase.list
RUN apt-get update && apt-get install -y libcouchbase-dev build-essential

RUN pip3 install pipenv

WORKDIR /app
COPY ./app/Pipfile /app/

RUN pipenv install --system --skip-lock

COPY ./app /app/

EXPOSE 8888

ENV FLASK_APP=app/main.py
ENV FLASK_DEBUG=1
CMD flask run --host=0.0.0.0 --port=8888