FROM nginx

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN mkdir -p /home/app/web/staticfiles
RUN mkdir -p /home/app/web/media
RUN mkdir -p /etc/ssl
COPY cert.crt /etc/ssl
COPY key.key /etc/ssl