# Bürokratt's widget 

# Scope
Set up a local Buerokratt widget within Buerokratt stack

### Requirements  
```docker```, ```docker-compose```

## Manual dev setup
 
Create a local project folder  ```widget```

Navigate inside created folder
Clone following repos and build images

- Clone [Ruuter](https://gitlab.ria.ee/BYK/Ruuter) ```git clone https://gitlab.ria.ee/BYK/Ruuter```
- Navigate to Ruuter, checkout dev branch ```git checkout dev``` and build the image `docker build -t ruuter .`
- Clone [Resql](https://gitlab.ria.ee/BYK/Resql) ```git clone https://gitlab.ria.ee/BYK/Resql```
- Navigate to Resql, checkout dev branch ```git checkout dev``` and build the image `docker build -t resql .`
- Clone [Chat Widget](https://gitlab.ria.ee/BYK/Chat-Widget) ```git clone https://gitlab.ria.ee/BYK/Chat-Widget```
- Navigate to, checkout dev branch ```git checkout dev``` build chat widget image `docker build -f Dockerfile.dev -t chat-widget .`
- Clone [Data Mapper](https://gitlab.ria.ee/BYK/DataMapper) ```git clone https://gitlab.ria.ee/BYK/DataMapper```
- Navigate to Data Mapper, checkout dev branch ```git checkout dev``` and build the image `docker build -t data-mapper .`

Run the stack with 
```
docker-compose up -d
```

With manual setup, you would also need to clone the [Buerokratt-Chatbot repo](https://gitlab.ria.ee/BYK/Buerokratt-Chatbot.git) for the necsessary DSL's and make sure, that these DSL's are correctly placed within your project folder. 

## Automatic dev setup

Create a local project folder ```widget```

Navigate inside created folder and copy the script ```run-widget-setup.sh```  
Run the set-up script  
```
bash run-widget-setup.sh
```  
