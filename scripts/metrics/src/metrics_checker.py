import requests_unixsocket
import json
import time
from utils import bytes_to_mb

session = requests_unixsocket.Session()

DOCKER_SOCKET_URL = 'http+unix://%2Fvar%2Frun%2Fdocker.sock'
LOG_FILE = '/data/metrics.log'

def get_container_stats(container_id):
    url = f"{DOCKER_SOCKET_URL}/containers/{container_id}/stats?stream=false"
    response = session.get(url)
    return response.json()

def log_metrics(metrics):
    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(metrics) + '\n')

def main():
    while True:
        containers_url = f"{DOCKER_SOCKET_URL}/containers/json"
        containers = session.get(containers_url).json()

        for container in containers:
            stats = get_container_stats(container['Id'])
            
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_cpu_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
            number_cpus = stats["cpu_stats"]["online_cpus"]

            cpu_percent = (cpu_delta / system_cpu_delta) * number_cpus * 100.0 if system_cpu_delta > 0.0 else 0.0
            memory_usage = stats["memory_stats"]["usage"]
            memory_limit = stats["memory_stats"]["limit"]
            memory_percent = (memory_usage / memory_limit) * 100.0

            networks = stats.get("networks", {})
            network_rx = sum(interface["rx_bytes"] for interface in networks.values())
            network_tx = sum(interface["tx_bytes"] for interface in networks.values())

            metrics = {
                "container_name": container["Names"][0],
                "cpu_percent": round(cpu_percent, 2),
                "memory_usage_mb": bytes_to_mb(memory_usage),
                "memory_percent": round(memory_percent, 2),
                "network_rx_mb": bytes_to_mb(network_rx),
                "network_tx_mb": bytes_to_mb(network_tx),
                "timestamp": stats["read"]
            }

            log_metrics(metrics)

        time.sleep(5)

if __name__ == "__main__":
    main()
