# DMR Helm chart

Deploys the Bürokratt Distributed Message Rooms server and, optionally, one or
more client-cluster DMR agents.

## Prerequisites

- Kubernetes 1.25+
- Helm 3
- RabbitMQ Cluster Operator when `rabbitmq.enabled=true`

The operator gives every RabbitMQ replica a separate `ReadWriteOnce` PVC. Queue
availability comes from RabbitMQ quorum replication; the replicas do not share
an RWX filesystem.

## Install a central server

```sh
helm upgrade --install dmr ./Kubernetes/Components/DMR \
  --namespace dmr --create-namespace \
  --set server.centops.configurationUrl=https://centops.example/api/configuration
```

For an external broker, set `rabbitmq.enabled=false`, configure
`rabbitmq.external.*`, and set `rabbitmq.auth.existingSecret`. The Secret must
contain `username` and `password` unless the key names are overridden.

Amazon MQ endpoints can be read from Secrets without hard-coding the generated
hostname:

```yaml
rabbitmq:
  enabled: false
  external:
    endpointSecretKeyRef:
      name: example-rabbitmq-connection
      key: instance_0_endpoint_0
    managementUriSecretKeyRef:
      name: example-rabbitmq-connection
      key: instance_0_console_url
  auth:
    existingSecret: example-rabbitmq-credentials
```

## Install an agent

Create the private-key Secret first:

```sh
kubectl -n dmr create secret generic dmr-agency-a-key \
  --from-file=private-key=./private.pem
```

Then use a values file:

```yaml
server:
  enabled: false
rabbitmq:
  enabled: false
agents:
  enabled: true
  serverWebSocketUrl: https://dmr.example.org
  items:
    - name: agency-a
      agentId: 00000000-0000-0000-0000-000000000000
      outgoingMessageEndpoint: http://chatbot:8080/api/messages
      existingSecret: dmr-agency-a-key
```

```sh
helm upgrade --install dmr-agent ./Kubernetes/Components/DMR \
  --namespace dmr --create-namespace -f agent-values.yaml
```
