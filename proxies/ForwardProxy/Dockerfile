FROM nginx:1.25.4-alpine AS web
COPY ./nginx/http-nginx.conf /etc/nginx/conf.d/default.conf
RUN apk add --no-cache bash
COPY ./nginx/scripts/env.sh /docker-entrypoint.d/env.sh
RUN chmod +x /docker-entrypoint.d/env.sh
EXPOSE 8090

ENTRYPOINT [ "bash", "/docker-entrypoint.d/env.sh" ]
