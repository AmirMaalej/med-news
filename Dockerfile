FROM python:3.6
ENV PYTHONBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt update && \
    apt install -y memcached
RUN pip3 install -r requirements.txt
ADD . /code
