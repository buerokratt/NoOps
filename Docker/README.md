#### About
Here is info needed for deployng services in a singular manner (docker-compose.yml will follow)
The yaml files from different repos have been written, concidering its own repo stucture 

##### RESQL
To deploy RESQL, clone the repo and update docker-compose.yml as shown in https://github.com/buerokratt/NoOps/blob/main/yaml/resql.yml  
Update `application.yml` according to https://github.com/buerokratt/NoOps/blob/main/docs/resql.md  
Run the following command   
`docker-compose up -d --build`

##### Dmapper  
Currently `handlebars` files are copied into a `byk` folder.

Example outcome  
`http://localhost:3000//byk/byk/notification_redirected_chat`
![image](https://user-images.githubusercontent.com/101868197/219674765-155cdd52-df07-4cb7-92da-bef6621aa246.png)

