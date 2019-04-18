FROM python:3.7

RUN mkdir /app

# fucken mother fuckern mysql i swear to god 

RUN apt-get update && apt-get install -y -q python3-dev default-libmysqlclient-dev mysql-server

# Time for the fun of ~~javascwipt~~
RUN apt-get install curl gnupg -yq
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install nodejs -yq

# Copy this explicitly first so we can cache

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

# hack to get this working cause i can't get it to install locally
RUN pip install mysqlclient

COPY . /app/web
RUN pip install /app/web/

EXPOSE 8000

WORKDIR /app/web

# install frontend
RUN cd frontend && npm install
RUN cd frontend && npm run build

CMD ["./run.sh"]
