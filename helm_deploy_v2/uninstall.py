import subprocess
import yaml
import sys
import os

def run_helm_command(command):
    """Run a Helm command and handle errors."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Helm: {e}")

def uninstall(deployment_name, namespace):
    """Uninstall a Helm release."""
    command = [
        'helm', 'uninstall', deployment_name,
        '--namespace', namespace
    ]
    
    print(f"Uninstalling {deployment_name} from {namespace} namespace...")
    try:
        run_helm_command(command)
        print(f"Uninstallation of {deployment_name} completed successfully.\n")
    except subprocess.CalledProcessError as e:
        if "release: not found" in str(e):
            print(f"Release {deployment_name} not found in namespace {namespace}. Skipping...\n")
        else:
            print(f"An error occurred while uninstalling {deployment_name}: {e}")
            sys.exit(1)

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

def main():
    if len(sys.argv) < 2:
        print("Usage: python uninstall.py <config_file> [deployment_name1 [deployment_name2 ...]]")
        sys.exit(1)

    config_file = sys.argv[1]
    deployment_names = sys.argv[2:]  # List of deployment names to uninstall

    deployments = load_config(config_file)

    if deployment_names:
        # Uninstall the specified deployments
        found_deployments = False
        for deployment in deployments:
            if deployment['name'] in deployment_names:
                uninstall(deployment['name'], deployment['namespace'])
                found_deployments = True

        if not found_deployments:
            print(f"None of the specified deployments were found in the config file.")
    else:
        # Uninstall all deployments
        for deployment in deployments:
            uninstall(deployment['name'], deployment['namespace'])

    print("Task failed successfully (Just joking, all is good).")

if __name__ == "__main__":
    main()
