# Deploying pgAdmin 4 on Kubernetes with Ingress

## Prerequisites

- Kubernetes cluster with `kubectl` access
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [Helm](https://helm.sh/docs/intro/install/) installed
- DNS/domain pointing to your Ingress 
- TLS secret created in your cluster
- Running PostgreSQL Service 

---


## 1. Create pgadmin-values.yaml

```
env:
  email: <EMAIL>
  password: <PASSWORD>

extraEnv:
  - name: PGADMIN_CONFIG_SERVER_ROOT
    value: "/pgadmin"

ingress:
  enabled: true
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
    nginx.ingress.kubernetes.io/configuration-snippet: |
      proxy_set_header X-Script-Name /pgadmin;
    nginx.ingress.kubernetes.io/whitelist-source-range: "<IP-YOU-WANT-TO-ALLOW/24"
  hosts:
    - host: <DOMAIN>
      paths:
        - path: /pgadmin(/|$)(.*)
          pathType: ImplementationSpecific
  tls:
    - hosts:
        - <DOMAIN>
      secretName: <CERT_SECRET>

service:
  type: ClusterIP
```
#### REPLACE the placeholder values

## 2. Deploy via Helm

```
helm repo add runix https://helm.runix.net/
```
```
helm repo update
```
```
helm install pgadmin runix/pgadmin4 \
  -n <NAMESPACE> \
  -f pgadmin-values.yaml
```  
#### REPLACE the placeholder values
