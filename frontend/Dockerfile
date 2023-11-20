FROM node:16.16.0

WORKDIR /star-burger/
COPY package.json /star-burger/
COPY package-lock.json /star-burger/

RUN npm ci --dev

COPY . /star-burger/

RUN ./node_modules/.bin/parcel watch bundles-src/index.js --dist-dir bundles --public-url="./"

