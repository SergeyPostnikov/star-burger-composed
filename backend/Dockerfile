FROM python:3.8.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV SECRET_KEY=12356jfcm.x/xS 

WORKDIR /star-burger/

COPY requirements.txt /star-burger/

RUN pip3 install -r requirements.txt
COPY . /star-burger/

RUN mkdir /star-burger/bundles/
