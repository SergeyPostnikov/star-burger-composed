FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/sites-availble/star-burger
RUN ln -s /etc/nginx/sites-available/star-burger /etc/nginx/sites-enabled
