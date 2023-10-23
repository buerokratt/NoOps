import os
import subprocess
import re
from config_train import *

def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Command failed: {command}")
        print(stderr.decode('utf-8'))
        exit(1)
    return stdout

# Import variables from config_train.py
config_file = "config_train.py"
if os.path.isfile(config_file):
    with open(config_file, "r") as file:
        config_content = file.read()
    exec(config_content)
else:
    print("[+] Configuration file not found. Make sure you have configured all values in the specified configuration file.")
    exit(1)

# Check for the existence of the repo without deletion
repo_path = "path-to/Training-Module"  # Define the full path to the repository
if os.path.isdir(repo_path):
    print("[+] Repo already exists: checking updates from git")
    execute_command(f"cd {repo_path} && git restore . && git fetch && git pull && git branch && git checkout dev && cd ../../")
else:
    print("[+] Cloning repo from git")
    execute_command(f"cd path-to/Training-Module && git clone https://github.com/buerokratt/Training-Module.git && cd Training-Module && git branch && git checkout dev && cd ../../")


if os.path.isfile(dockerfile_path):
    with open(dockerfile_path, "r") as file:
        dockerfile_content = file.read()

    # Modify the content to replace "FROM node:<old_version>" with "FROM node:<new_version>"
    dockerfile_content = re.sub(r'FROM node:[0-9.]+', f'FROM node:{node_version}', dockerfile_content)
    if dockerfile_content != dockerfile_content:
        print("NODE Dockerfile was successfully modified.")
    else:
        print("NODE Dockerfile was not modified as expected.")
    
    # Write the updated content back to the Dockerfile
    with open(dockerfile_path, "w") as file:
        file.write(dockerfile_content)
else:
    print(f"Dockerfile not found at {dockerfile_path}")
    exit(1)

if os.path.isfile(gui_dockerfile):
    with open(gui_dockerfile, "r") as file:
        dockerfile_content = file.read()
    dockerfile_content = re.sub(r'COPY \./package\*.json \./', f'COPY ./package*.json ./\n{line_to_insert}', dockerfile_content, count=1)

    if line_to_insert != dockerfile_content:
        print("GUI Dockerfile was successfully modified.")
    else:
        print("GUI Dockerfile was not modified as expected.")
    
    # Write the updated content back to the Dockerfile
    with open(gui_dockerfile, "w") as file:
        file.write(dockerfile_content)
else:
    print(f"Dockerfile not found at {gui_dockerfile}")
    exit(1)

# Check dockre-compose.yml
if os.path.isfile(dockercomposepath):
    with open(dockercomposepath, "r") as file:
        docker_compose_content = file.read()
    
else:
    print(f"Docker Compose file not found at {dockercomposepath}")
    exit(1)

# Modify RUUTER
ruuter_pattern = re.compile(r'ruuter:\s+container_name: byk-private-ruuter\n\s+build:\s+context: .*?\n\s+dockerfile: .*?$', re.MULTILINE)
docker_compose_content = re.sub(ruuter_pattern, f'ruuter:\n    container_name: byk-private-ruuter\n    image: {ruuterimage}', docker_compose_content, count=1)
docker_compose_content = re.sub(r'ports:\n\s+- 8080:8080', f'ports:\n      - {ruuter_ports[0]}:{ruuter_ports[1]}', docker_compose_content)

if ruuter_ports != dockerfile_content:
        print("Ruuter in docker-compose was successfully modified.")
else:
        print("Ruuter in docker-compose was not modified as expected.")
    
# Modify RESQL
resql_pattern = re.compile(r'resql:\s+container_name: byk-resql\n\s+build:\s+context: .*?\n\s+dockerfile: .*?$', re.MULTILINE)
docker_compose_content = re.sub(resql_pattern, f'resql:\n    container_name: byk-resql\n    image: {resqlimage}', docker_compose_content, count=1)
docker_compose_content = re.sub(r'ports:\n\s+- 8082:8082', f'ports:\n      - {resql_ports[0]}:{resql_ports[1]}', docker_compose_content)

if resqlimage != dockerfile_content:
        print("RESQL in docker-compose was successfully modified.")
else:
        print("RESQL in docker-compose was not modified as expected.")
    
# Modify Node and GUI
node_service_pattern = re.compile(r'node:\s+container_name: node\n\s+build:\s+context: .*', re.MULTILINE)
docker_compose_content = re.sub(r'- ./mock1:/mock1', '- ./mock1:/mock2', docker_compose_content)

docker_compose_content = re.sub(r'ports:\n\s+- 3000:3000', f'ports:\n      - {node_ports[0]}:{node_ports[1]}', docker_compose_content)
docker_compose_content = re.sub(r'ports:\n\s+- 3001:80', f'ports:\n      - {training_gui_ports[0]}:{training_gui_ports[1]}', docker_compose_content)

    

with open(dockercomposepath, "w") as file:
    file.write(docker_compose_content)

# Define the content to be written
env_content = f"""REACT_APP_API_URL={REACT_APP_API_URL}
REACT_APP_RUUTER_V1_PRIVATE_API_URL={REACT_APP_RUUTER_V1_PRIVATE_API_URL}
REACT_APP_RUUTER_V2_PRIVATE_API_URL={REACT_APP_RUUTER_V2_PRIVATE_API_URL}
REACT_APP_RUUTER_V2_ANALYTICS_API_URL={REACT_APP_RUUTER_V2_ANALYTICS_API_URL}
REACT_APP_BUEROKRATT_CHATBOT_URL={REACT_APP_BUEROKRATT_CHATBOT_URL}
REACT_APP_OPENSEARCH_DASHBOARD_URL={REACT_APP_OPENSEARCH_DASHBOARD_URL}
REACT_APP_OPENDATAPORT_URL={REACT_APP_OPENDATAPORT_URL}
REACT_APP_MENU_URL={REACT_APP_MENU_URL}
REACT_APP_MENU_PATH={REACT_APP_MENU_PATH}
REACT_APP_APP_PORT={REACT_APP_APP_PORT}
REACT_APP_LOCAL={REACT_APP_LOCAL}
REACT_APP_BASE_API_PATH={REACT_APP_BASE_API_PATH}
REACT_APP_AUTH_BASE_URL={REACT_APP_AUTH_BASE_URL}
REACT_APP_AUTH_PATH={REACT_APP_AUTH_PATH}
REACT_APP_CUSTOMER_SERVICE_LOGIN={REACT_APP_CUSTOMER_SERVICE_LOGIN}
REACT_APP_CONVERSATIONS_BASE_URL={REACT_APP_CONVERSATIONS_BASE_URL}
REACT_APP_TRAINING_BASE_URL={REACT_APP_TRAINING_BASE_URL}
REACT_APP_ANALYTICS_BASE_URL={REACT_APP_ANALYTICS_BASE_URL}
REACT_APP_SERVICES_BASE_URL={REACT_APP_SERVICES_BASE_URL}
REACT_APP_SETTINGS_BASE_URL={REACT_APP_SETTINGS_BASE_URL}
REACT_APP_MONITORING_BASE_URL={REACT_APP_MONITORING_BASE_URL}
REACT_APP_SERVICE_ID={REACT_APP_SERVICE_ID}
"""

# Define the path to .env.development
env_path = "path-to/Training-Module/GUI/.env.development"

# Write the content to .env.development
with open(env_path, "w") as file:
    file.write(env_content)

print("[+] .env.development file updated")
# Run it all
print("[+] Running containers")
training_module_path = "path-to/Training-Module"
execute_command(f"cd path-to/Training-Module && docker-compose up -d --build && cd ../../")
#execute_command(f"cd Training-Module && docker-compose up -d && cd ../../")
