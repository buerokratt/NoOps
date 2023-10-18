### About  
Here is the script, config.ini and quick tutorial for database/databases deployment and seeding using a python script  

##### Script and configuration  
Make sure to replace the calues in `config.ini` according to what you are using
config.ini example:  
```
[PostgreSQL]
username = test
password = test123
postgres_db = test_db
postgres_port = 5555
postgres_container = test_postgre_db
postgres_image = postgres:latest
liquibase_container = test_liquibase
liquibase_image = liquibase/liquibase:latest
master_yml = /path/to/location/master.yml
changelog = /path/to/location/changelog
```

Run the script  
```
python3 postgre.py
```

##### Database updating   
To be filled.
