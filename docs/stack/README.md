# Bürokratt's widget 

# Scope
Set up a local Buerokratt widget within Buerokratt stack

### Requirements  
```docker```, ```docker-compose```

## Manual dev setup
 
Create a local project folder  ```widget```

Navigate inside created folder
Clone following repos and build images

- Clone [Ruuter](https://github.com/buerokratt/Ruuter) ```git clone https://github.com/buerokratt/Ruuter```
- Navigate to Ruuter, checkout dev branch ```git checkout dev``` and build the image `docker build -t ruuter .`
- Clone [Resql](https://github.com/buerokratt/Resql) ```git clone https://github.com/buerokratt/Resql```
- Navigate to Resql, checkout dev branch ```git checkout dev``` and build the image `docker build -t resql .`
- Clone [Chat Widget](https://github.com/buerokratt/Chat-Widget) ```git clone https://github.com/buerokratt/Chat-Widget```
- Navigate to, checkout dev branch ```git checkout dev``` build chat widget image `docker build -f Dockerfile.dev -t chat-widget .`
- Clone [Data Mapper](https://github.com/buerokratt/DataMapper) ```git clone https://github.com/buerokratt/DataMapper```
- Navigate to Data Mapper, checkout dev branch ```git checkout dev``` and build the image `docker build -t data-mapper .`

Run the stack with 
```
docker-compose up -d
```

## Automatic dev setup

Create a local project folder ```widget```

Navigate inside created folder and copy the script ```run-widget-setup.sh```  
Run the set-up script  
```
bash run-widget-setup.sh
```  
