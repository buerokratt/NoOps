import os
import subprocess
import re
import shutil
from config_base import *
from colorama import Fore, Style

print(f"{Fore.GREEN}Let's GO!!!{Style.RESET_ALL}")

# Set up config
def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Command failed: {command}")
        print(stderr.decode('utf-8'))
        exit(1)
    return stdout

# Import variables from config_service.py
config_file = "config_base.py"
if os.path.isfile(config_file):
    with open(config_file, "r") as file:
        config_content = file.read()
    exec(config_content)
else:
    print("[+] Configuration file not found.")
    exit(1)

# Git clone desired repo. In case of it already existing, git fetch and pull (restore if needed)
repo_path = "Service-Module"
if os.path.isdir(repo_path):
    print("[+] Repo already exists: checking updates from git")
    execute_command(f"cd {repo_path} && git restore . && git fetch && git pull && git branch && git checkout dev && cd ../../")
else:
    print("[+] Cloning repo from git")
    execute_command(f" git clone https://github.com/buerokratt/Service-Module.git && cd Service-Module && git branch && git checkout dev && cd ../../")

# Copy files
if not copy_files:
    print("No info in config.py, skipping copy_files")
else:

    for source, destination in copy_files:
        if source and destination:
            if not os.path.exists(destination) or os.path.realpath(source) != os.path.realpath(destination):
                shutil.copy(source, destination)

# Change Dockerfile
if os.path.isfile(node_dockerfile):
    with open(node_dockerfile, "r") as file:
        dockerfile_content = file.read()

dockerfile_modifications = {
    node_dockerfile: [
        (rf'FROM node:[0-9.]+ AS development', f'FROM node:{node_version} AS development')
    ],
}

for dockerfile_path, modifications in dockerfile_modifications.items():
    if os.path.isfile(dockerfile_path):
        with open(dockerfile_path, "r") as file:
            dockerfile_content = file.read()

        for old_text, new_text in modifications:
            dockerfile_content = re.sub(old_text, new_text, dockerfile_content)

        with open(dockerfile_path, "w") as file:
            file.write(dockerfile_content)
    else:
        print(f"Dockerfile not found at {dockerfile_path}")
        exit(1)
print(f"{Fore.BLUE}CHECK{Fore.RED}POINT{Style.RESET_ALL}")
# Check dockre-compose.yml
if os.path.isfile(docker_compose_path):
    with open(docker_compose_path, "r") as file:
        docker_compose_content = file.read()
    
else:
    print(f"docker-compose file not found at {docker_compose_path}")
    exit(1)
# Docker-compose changes
docker_compose_modifications = {
    "docker-compose.yml": [
        (r'ruuter:\s+container_name: ruuter\n\s+image: ruuter', f'ruuter:\n    container_name: {ruuter_container}\n    image: {ruuter_image}'),
        (r'environment:\n\s+- application.cors.allowedOrigins=http://localhost:3006,http://localhost:3001,http://localhost:8085', f'environment:\n      - application.cors.allowedOrigins={ruuter_cors}'),
        (r'ports:\n\s+- 8085:8085', f'ports:\n      - {ruuter_ports[0]}:{ruuter_ports[1]}'),
            (
        f'volumes:\n',  # Replace this line under volumes
        f'volumes:\n      - ./test.ini:/app/test.ini',  # Add this line under volumes
            ),
        (r'resql:\s+container_name: resql\n\s+image: resql', f'resql:\n    container_name: {resql_container}\n    image: {resql_image}'),
        (r'ports:\n\s+- 8087:8087', f'ports:\n      - {resql_ports[0]}:{resql_ports[1]}'),
        (r'sqlms.datasources.\[0\].name=services', f'sqlms.datasources.[0].name={resql_db_name}'),
        (r'sqlms.datasources.\[0\].jdbcUrl=jdbc:postgresql://database:5432/services_db', f'sqlms.datasources.[0].jdbcUrl={resql_db_url}'),
        (r'sqlms.datasources.\[0\].username=byk', f'sqlms.datasources.[0].username={resql_db_user}'),
        (r'sqlms.datasources.\[0\].password=01234', f'sqlms.datasources.[0].password={resql_db_password}'),
        (r'resql-users:\s+container_name: resql-users\n\s+image: resql', f'resql:\n    container_name: {resql_users_container}\n    image: {resql_image}'),
        (r'ports:\n\s+- 8088:8088', f'ports:\n      - {resql_users_ports[0]}:{resql_users_ports[1]}'),
        (r'sqlms.datasources.\[0\].name=users', f'sqlms.datasources.[0].name={resql_users_db_name}'),
        (r'sqlms.datasources.\[0\].jdbcUrl=jdbc:postgresql://database:5432/users_db', f'sqlms.datasources.[0].jdbcUrl={resql_users_db_url}'),
        (r'sqlms.datasources.\[0\].username=byk', f'sqlms.datasources.[0].username={resql_users_db_user}'),
        (r'sqlms.datasources.\[0\].password=01234', f'sqlms.datasources.[0].password={resql_users_db_password}'),
        (r'database:\s+container_name: database\n\s+image: postgres:14.1', f'resql:\n    container_name: {database_container}\n    image: {database_image}'),
        (r'- POSTGRES_USER=byk', f'- POSTGRES_USER={postgres_user}'),
        (r'- POSTGRES_PASSWORD=01234', f'- POSTGRES_PASSWORD={postgres_password}'),
        (r'- POSTGRES_MULTIPLE_DATABASES=users_db,services_db', f'- POSTGRES_MULTIPLE_DATABASES={resql_db_name,resql_users_db_name}'),
        (r'ports:\n\s+- 5433:5432', f'ports:\n      - {database_ports[0]}:{database_ports[1]}'),
        (r'data_mapper:\s+container_name: data_mapper\n\s+image: datamapper-node', f'data_mapper:\n    container_name: {dmapper_container}\n    image: {dmapper_image}'),
        (r'ports:\n\s+- 3005:3005', f'ports:\n      - {dmapper_ports[0]}:{dmapper_ports[1]}'),
     # This is example to remove the docker build part and replace with image
     #   (
     #    r'node_server:\s+container_name: node_server\n\s+build:\s+context: .*?\n\s+dockerfile: .*?$',
     #    f'node_server:\n    container_name: {node_container}\n    image: {node_image}',
     #   ),
        (f'node_server:\n    ports:\n\s+- 3005:3005', f'ports:\n      - {node_port[0]}:{node_port[1]}'),
        (r'gui_dev:\s+container_name: gui_dev\n\s+', f'gui_dev:\n    container_name: {gui_container}\n    '),
    ],
}

# Check if any modifications were made
modifications_made = any(old_text != new_text for old_text, new_text in modifications)

if modifications_made:
    print(f"{Fore.GREEN}Docker-compose change was successful{Style.RESET_ALL}")
else:
    print(f"{Fore.GRAY}No changes made to docker-compose{Style.RESET_ALL}")

#print(f"{Fore.YELLOW}[+] docker-copose.yml updated{Style.RESET_ALL}")

# Define the path to .env.development
env_path = "Service-Module/GUI/.env.development"
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

# Write the content to .env.development
with open(env_path, "w") as file:
    file.write(env_content)

print(f"{Fore.YELLOW}[+] .env.development file updated{Style.RESET_ALL}")

#.env file change
env_file_path = "Service-Module/GUI/.env" 

# Check if the .env file exists and write the content
if os.path.isfile(env_file_path):
    with open(env_file_path, "w") as file:
        file.write(gui_env)
else:
    print(f".{Fore.RED}.env not found at {env_file_path} {Style.RESET_ALL}")
    exit(1)
print(f"{Fore.YELLOW}[+] .env file updated{Style.RESET_ALL}")

# Run it all
 print("[+] Running containers")

execute_command(f"cd Service-Module && docker-compose up -d --build && cd ../../")

# Final debug
print(f"{Fore.BLUE}Finished{Style.RESET_ALL}")
print(f"{Fore.BLUE}Enjoy the Ruuter{Style.RESET_ALL}")
