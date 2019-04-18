FROM python:3.7

# Install postgres client to enable db waiting

RUN apt-get update && apt-get install -y -q postgresql-client

RUN mkdir /app

# Copy this explicitly first so we can cache

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

COPY . /app/web
RUN pip install /app/web/

EXPOSE 8000

WORKDIR /app/web

CMD ["./run.sh"]
