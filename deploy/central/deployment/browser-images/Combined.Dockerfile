ARG CHATBOT_IMAGE
ARG WIDGET_IMAGE
ARG SERVICE_IMAGE
ARG CKB_IMAGE
ARG LLM_IMAGE
FROM ${CHATBOT_IMAGE} AS chatbot
FROM ${WIDGET_IMAGE} AS widget
FROM ${SERVICE_IMAGE} AS service
FROM ${CKB_IMAGE} AS ckb
FROM ${LLM_IMAGE} AS llm
FROM nginx:1.25.4-alpine@sha256:a8b39bd9cf0f83869a2162827a0caf6137ddf759d50a171451b335cecc87d236 AS runtime
COPY --from=chatbot /usr/share/nginx/html/chat /usr/share/nginx/html/chat
COPY --from=chatbot /usr/share/nginx/html/login.html /usr/share/nginx/html/login.html
COPY --from=widget /usr/share/nginx/html/widget /usr/share/nginx/html/widget
COPY --from=service /usr/share/nginx/html/services /usr/share/nginx/html/services
COPY --from=ckb /usr/share/nginx/html/ckb /usr/share/nginx/html/ckb
COPY --from=llm /usr/share/nginx/html/rag-search /usr/share/nginx/html/rag-search
COPY deployment/browser-images/nginx-main.conf /etc/nginx/nginx.conf
USER 1000:1000
ENTRYPOINT ["nginx","-g","daemon off;"]
