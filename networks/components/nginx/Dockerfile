FROM nginx:1.13
RUN mkdir -p /etc/nginx/html/ && touch /etc/nginx/html/index.html
RUN echo 'Hi, I am in your container' \
  >/usr/share/nginx/html/index.html
EXPOSE 80
