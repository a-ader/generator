version: '3.7'

services:
  mysql:
    image: mysql:5.7
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: "123123"
    volumes:
      - mysql-data:/var/lib/mysql

  redis:
    image: redis

  app:
    image: ${APP_IMAGE}
    restart: always
    volumes:
      - media:/var/www/var/media

    environment:
      DJANGO_SETTINGS_MODULE: app.settings_prod

  nginx:
    image: ${NGINX_IMAGE}
    restart: always
    networks:
      - proxy
      - default

    deploy:
      labels:
        - "traefik.port=80"
        - "traefik.frontend.rule=PathPrefix:/"
        - "traefik.frontend.rule=Host:${APP_HOSTNAME}"
        - "traefik.docker.network=proxy"

    volumes:
      - media:/var/www/var/media

networks:
  default:
    external: false
  proxy:
    external: true

volumes:
 media:
 mysql-data: