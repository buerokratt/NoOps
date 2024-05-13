FROM python:3.12.3

RUN apt-get update && \
    apt-get install -y apt-transport-https && \
    apt-get update && \
    apt-get install -y curl && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl && \
    rm kubectl
RUN pip install kubernetes
RUN pip install pyyaml

RUN wget -qO- https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

WORKDIR /app

COPY centops.py /app/centops.py

COPY kubeconfig.yaml /root/.kube/config

CMD ["python", "centops.py"]
