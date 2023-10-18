import subprocess
import time
import configparser

# Read the PostgreSQL info from the config file
config = configparser.ConfigParser()
config.read('config.ini')

postgres_username = config['PostgreSQL']['username']
postgres_password = config['PostgreSQL']['password']
postgres_db = config['PostgreSQL']['postgres_db']
postgres_ip = config['PostgreSQL']['postgres_ip']
postgres_port = config['PostgreSQL']['postgres_port']
postgres_container = config['PostgreSQL']['postgres_container']
postgres_image = config['PostgreSQL']['postgres_image']
liquibase_container = config['PostgreSQL']['liquibase_container']
liquibase_image = config['PostgreSQL']['liquibase_image']

# Check if the PostgreSQL container is already running, if it is, stop and remove
check_command = f"docker ps --filter name={postgres_container} --format '{{.Names}}'"
running_container = subprocess.check_output(check_command, shell=True).strip()

if running_container:
    stop_command = f"docker stop {postgres_container}"
    remove_command = f"docker rm {postgres_container}"
    subprocess.run(stop_command, shell=True)
    subprocess.run(remove_command, shell=True)

# Start a Postgres Docker container
postgres_container_cmd = f"docker run --name {postgres_container} -e POSTGRES_PASSWORD={postgres_password} -p {postgres_port}:5432 -e POSTGRES_DB={postgres_db} -e POSTGRES_USER={postgres_username} -d {postgres_image}"
subprocess.run(postgres_container_cmd, shell=True)

# Wait for the container to be up and running
time.sleep(10)

# Liquibase build and seeding the database
liquibase_cmd = f"docker run --name {liquibase_container} -v ./DSL/Liquibase/changelog:/liquibase/changelog -v ./DSL/Liquibase/master.yml:/liquibase/master.yml {liquibase_image} --url=jdbc:postgresql://{postgres_ip}:{postgres_port}/{postgres_db} --username={postgres_username} --password={postgres_password} --changeLogFile=master.yml update -Dliquibase.hub.mode=OFF"

# Run Liquibase to apply your changes to the "train_db" database
subprocess.run(liquibase_cmd, shell=True)

# Debug line

# Stop and remove Liquibase container
subprocess.run(f"docker stop {liquibase_container}", shell=True)
subprocess.run(f"docker rm {liquibase_container}", shell=True)


print("Database has been set up and updated.")
