# Custom Docker Metrics Checker

This is a lightweight metrics collector for Docker containers, capturing:
- CPU usage
- Memory usage
- Network traffic

Metrics are logged to `/data/metrics.log` inside the container (mount this to a PVC in Kubernetes or a local folder).

## 📦 Usage

### Local

```bash
docker build -t custom-metrics-checker .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd)/data:/data custom-metrics-checker
```

### K8s  
To be added
