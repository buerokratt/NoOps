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

### 🛠️ Dev Shortcuts

Using the provided `Makefile`:

```bash
# Build the image
make build


# Run the container locally
make run

# View collected logs
make logs

# Clean the Docker image
make clean

# Use docker-compose
make compose-up   # to start
make compose-down # to stop
```

### 🐳 Local Docker (manual)

Build and run:
```bash
docker build -t custom-metrics-checker .
docker run -v /var/run/docker.sock:/var/run/docker.sock -v $(pwd)/data:/data custom-metrics-checker
```

### ☸️ K8s  
Run:  

```
kubectl apply -f k8s/pvc.yaml
```

```
kubectl apply -f k8s/deployment.yaml
```
