# 🐳 Custom Docker Metrics Checker

A lightweight metrics collector for Docker containers, capturing:
- CPU usage
- Memory usage
- Network traffic

Metrics are logged as JSON lines to `/data/metrics.log`.

## 📦 How it Works

- Accesses the Docker API via Unix socket
- Gathers live container stats
- Logs CPU %, memory usage (MB and %), and network RX/TX in MB
- Outputs to a mounted `/data` directory (local or PVC in Kubernetes)

## 🚀 Usage

### Local Docker

Build and run:
```bash
docker build -t custom-metrics-checker .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd)/data:/data custom-metrics-checker
```

### K8s  
Run:  

```
kubectl apply -f k8s/pvc.yaml
```

```
kubectl apply -f k8s/deployment.yaml
```
