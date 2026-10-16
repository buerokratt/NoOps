FROM python:3.13-alpine@sha256:2d9aefe2fef018a7eb2c13064c89c71929800fd2e5dccdbf52ea5da5bb8d929a AS runtime
COPY deployment/bundle/ /bundle/
COPY deployment/package-assets/seed_files.py /app/seed_files.py
USER 1000:1000
CMD ["python3","-B","/app/seed_files.py"]
