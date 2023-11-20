FROM python:3.8.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /star-burger/


COPY requirements.txt /star-burger/

# RUN apt install -y python3-pip                                  \
#     && pip3 install -r requirements.txt                                       \
#     && apt remove -y python3-pip                                              \
#     && apt autoremove --purge -y                                              \
#     && rm -rf /var/lib/apt/lists/*
RUN pip3 install -r requirements.txt
COPY . /star-burger/

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python3", "manage.py", "migrate", "--noinput"]
