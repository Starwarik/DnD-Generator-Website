FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf

RUN mkdir -p /var/www/dnd-webapp
RUN mkdir -p /etc/letsencrypt/live/adventuregenerator.ru

COPY ./web /var/www/dnd-webapp

EXPOSE 443
EXPOSE 8004

CMD ["nginx", "-g", "daemon off;"]
