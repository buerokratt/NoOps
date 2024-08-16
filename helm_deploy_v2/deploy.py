import subprocess
import yaml
import sys
import os
import time

def run_helm_command(command):
    """Run a Helm command and handle errors."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Helm: {e}")
        sys.exit(1)

def check_and_create_namespace(namespace):
    """Check if a Kubernetes namespace exists, and create it if it doesn't."""
    try:
        # Check if namespace exists
        result = subprocess.run(
            ['kubectl', 'get', 'namespace', namespace],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            print(f"Namespace '{namespace}' does not exist. Creating it...")
            # Create the namespace
            subprocess.run(['kubectl', 'create', 'namespace', namespace], check=True)
            print(f"Namespace '{namespace}' created successfully.")
        else:
            print(f"Namespace '{namespace}' already exists.")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while checking or creating the namespace: {e}")
        sys.exit(1)

def interactive_delay(duration):
    
    countdown_messages = [
        "Two minutes is a long time... Go get some coffee",
        "Patience is a virtue you know.",
        "Almost...there...",
        "Final seconds... lets hope it wont go KABOOM"
    ]
    
    interval = 15  # Update every 15 seconds
    for i in range(0, duration, interval):
        remaining = duration - i
        print(f"{remaining} seconds remaining... {countdown_messages[i // interval]}")
        time.sleep(interval)
    
    print("Time's up! Proceeding with the next deployment...")

def deploy(deployment):
    """Deploy using Helm based on the deployment configuration."""
    name = deployment['name']
    chart_path = deployment['chart_path']
    namespace = deployment['namespace']

    # Check and create namespace if it does not exist
    check_and_create_namespace(namespace)

    command = [
        'helm', 'upgrade', '--install', name, chart_path,
        '--namespace', namespace
    ]

    # Check if 'values_file' is provided and add it to the command if present
    if 'values_file' in deployment:
        values_file = deployment['values_file']
        command.extend(['-f', values_file])

    print(f"Deploying {name} to {namespace} namespace...")
    run_helm_command(command)
    print(f"Deployment {name} completed successfully.\n")

    # Introduce a 1-minute delay after deploying 'component-databases'
    if name == 'component-databases':
        print("Waiting for a minute before proceeding with the next deployment...")
        interactive_delay(60)  # Wait for 60 seconds interactively

def load_config(config_file):
    """Load deployments configuration from a YAML file."""
    if not os.path.exists(config_file):
        print(f"Config file {config_file} does not exist.")
        sys.exit(1)

    with open(config_file, 'r') as file:
        try:
            config = yaml.safe_load(file)
            return config.get('deployments', [])
        except yaml.YAMLError as e:
            print(f"Error parsing the config file: {e}")
            sys.exit(1)

def process_file(file_name, filters=None):
    """Process deployments from a given file with optional filters."""
    deployments = load_config(file_name)
    for deployment in deployments:
        if filters is None or deployment['name'] in filters:
            deploy(deployment)

def main():
    if len(sys.argv) < 2:
        print("Usage: python deploy.py <file1.yaml> [<file2.yaml> ...] [deployment_name]")
        sys.exit(1)

    # Collect all file arguments (excluding the script name)
    files = sys.argv[1:]
    target_deployment = None

    # Check if the last argument is a deployment name (filter)
    if len(files) > 1 and (files[-1].startswith('component-') or files[-1].startswith('module-')):
        target_deployment = files.pop()

    for file_name in files:
        process_file(file_name, filters=[target_deployment] if target_deployment else None)

if __name__ == "__main__":
    main()
