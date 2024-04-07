FROM python:3.9

MAINTAINER "Adrián Ramos"
ENV APP_DIR /server/app/challenge/infrastructure/django_project/

RUN mkdir /server

ADD ./app /server/app
ADD ./lib /server/lib
ADD ./etc /server/etc

ADD wait-for-it.sh $APP_DIR

RUN pip install --upgrade pip
RUN pip install -r /server/etc/app/challenge/requirements.txt

WORKDIR $APP_DIR

EXPOSE 8000