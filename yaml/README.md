#### About
Here is info needed for deployng services in a singular manner (docker-compose.yml will follow)
The yaml files from different repos have been written, concidering its own repo stucture 

##### RESQL
To deploy RESQL, clone the repo and update docker-compose.yml as shown in https://github.com/buerokratt/NoOps/blob/main/yaml/resql.yml  
Update `application.yml` according to https://github.com/buerokratt/NoOps/blob/main/docs/resql.md  
Run the following command   
`docker-compose up -d --build`
