import subprocess
import sys
import os
import yaml

def run_git_command(command):
    """Run a Git command and handle errors."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running Git: {e}")
        sys.exit(1)

def clone_repository(repo_url):
    """Clone a Git repository into the current directory."""
    # Extract the repo name from the URL for directory creation
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    
    # Ensure the target directory does not exist, or remove it if it does
    if os.path.exists(repo_name):
        print(f"Directory {repo_name} already exists. Removing...")
        subprocess.run(['rm', '-rf', repo_name], check=True)
    
    # Perform the Git clone
    command = ['git', 'clone', repo_url]
    print(f"Cloning repository from {repo_url} into the current directory...")
    run_git_command(command)
    print(f"Repository cloned successfully into {repo_name}.\n")

def load_git_config(config_file):
    """Load Git repository configuration from a YAML file."""
    if not os.path.exists(config_file):
        print(f"Config file {config_file} does not exist.")
        sys.exit(1)

    with open(config_file, 'r') as file:
        try:
            config = yaml.safe_load(file)
            repo_url = config.get('repository', {}).get('url')
            if not repo_url:
                print("Repository URL is not defined in the config file.")
                sys.exit(1)
            return repo_url
        except yaml.YAMLError as e:
            print(f"Error parsing the config file: {e}")
            sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python clone_repo.py <git_config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    repo_url = load_git_config(config_file)
    clone_repository(repo_url)

if __name__ == "__main__":
    main()
