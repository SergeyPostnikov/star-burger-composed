FROM node:16.16.0

WORKDIR /star-burger/
COPY package.json /star-burger/
COPY package-lock.json /star-burger/

RUN npm ci --dev

COPY . /star-burger/

