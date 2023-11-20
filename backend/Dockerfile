FROM python:3.8.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /star-burger/

COPY requirements.txt /star-burger/

RUN pip3 install -r requirements.txt
COPY . /star-burger/

RUN mkdir /star-burger/bundles/

RUN python3 manage.py collectstatic --noinput --clear
RUN python3 manage.py migrate --noinput

CMD ["gunicorn" "star_burger.wsgi:application" "--bind" "0.0.0.0:8000"]
