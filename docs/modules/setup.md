## Architectural Guidebook for Analytics Module

### 3. Setup Instructions

#### Development Setup

1. **Cloning the Repository**
   - Open your terminal and run the following command to clone the repository:
     ```bash
     git clone https://gitlab.ria.ee/BYK/Analytics-Module.git
     cd Analytics-Module
     ```
   
2. **Building Necessary Images**
   - Navigate to each subdirectory and build the Docker images:
     ```bash
     # For Ruuter
     cd Ruuter
     docker build -t ruuter .

     # For Resql
     cd ../Resql
     docker build -t resql .

     # For Data Mapper
     cd ../DataMapper
     docker build -t data-mapper .

     # For TIM
     cd ../TIM
     docker build -t tim .

     # For Cron Manager
     cd ../CronManager
     docker build -t cron-manager .
     ```

3. **Running the Application Locally**
   - Ensure that you have Docker Compose installed. Run the following command to start all services:
     ```bash
     docker compose up -d
     ```
   - Once the services are running, access the application at [http://localhost:3001](http://localhost:3001).

#### Database Setup

1. **Initial Database Configuration**
   - To set up the database, run the following command:
     ```bash
     docker run --platform linux/amd64 --network=bykstack riaee/byk-users-db:liquibase20220615 --url=jdbc:postgresql://users_db:5432/byk --username=byk --password=01234 --changelog-file=./master.yml update
     ```

2. **Running Migrations**
   - To apply migrations included in the repository, execute the helper script:
     ```bash
     ./migrate.sh
     ```

3. **Creating Default Users**
   - To add a default user and bot configuration, run this command while the `users_db` container is running:
     ```bash
     docker exec users_db psql byk byk -c "INSERT INTO public.\"user\" (login,password_hash,first_name,last_name,id_code,display_name,status,created) VALUES ('EE90009999999','t','t','t','EE90009999999','t',NULL,NULL);"
     docker exec users_db psql byk byk -c "INSERT INTO public.\"configuration\" (\"key\",value) VALUES ('bot_institution_id','botname');"
     ```

#### Common Pitfalls
- Ensure Docker is running before executing any Docker commands.
- Check for any network issues if the application is not accessible at the specified URL.
- Verify that the correct permissions are set for the migration scripts.

#### Conclusion
Following these setup instructions will allow developers to run the Analytics Module locally, enabling them to contribute effectively. If any issues arise during setup, refer to the troubleshooting section or seek assistance from the team.
