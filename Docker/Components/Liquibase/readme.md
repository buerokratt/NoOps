#### About  
##### Here is described how to seed your Postgres database using Liquibase  

Change the parameters of `docker-compose.yml` to show where liquibase will get the `master.yml` and `changelog`  

Following examples show how run liquibase on Training-module enviornment

##### Structure example  
```
- Work_folder
  - Liquibase
    - changelog
      - 202304151112_file_that_updates_table.xml 
    - master.yml
```
##### docker-compose example

```
version: '3.9'

services:

   byk-liquibase-update:
    image: liquibase/liquibase
    command: --url=jdbc:postgresql://database_address:5433/byk?user=byk --password= --changelog-file=/master.yml update
    ports:
      - 8000:8000
    volumes:
      - ./Liquibase/master.yml:/liquibase/master.yml
      - ./Liquibase/changelog:/liquibase/changelog
    networks:
      - bykstack
      
networks:
  bykstack:
    name: bykstack
    driver: bridge
    driver_opts:                         
       com.docker.network.driver.mtu: 1400
```

#### Followups  
When you run a single Postgres you can either run everything in a single database(1) or create database for every module(2).
 1) Do not change the database name (leave it as byk). Gather the DSL's into a singular spot (every module DSL in a same folder)
 2) DSL are separated my modules. Create a database for every module.

##### How to create a Postgres database for modules
Here is shown how to create Postgres databases for every singuar module.  
Example Postgres container name is `users-db`  
Enter the container
```
docker exec -it users-db bash
```
Create a new database ( for example `treening`)
```
createdb -U byk treening
```
To seed the new database make sure to change following line in `docker-compose.yml`    
```
command: --url=jdbc:postgresql://database_address:5433/byk?user=byk --password= --changelog-file=/master.yml update
```
into
```
command: --url=jdbc:postgresql://database_address:5433/treening?user=byk --password= --changelog-file=/master.yml update
```

##### RESQL
To make sure, that your RESQL container can connect to your database, replace database name to mirror the correct one
