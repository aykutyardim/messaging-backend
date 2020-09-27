FROM python:3.8-slim-buster
LABEL maintainer="Messaging-app"

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:${PATH}"

RUN pip install --upgrade pip
RUN apt-get update
RUN apt-get clean

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /messaging_app
WORKDIR /messaging_app
COPY ./messaging_app /messaging_app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN adduser --disabled-password --gecos '' user
USER user

CMD ["entrypoint.sh"]