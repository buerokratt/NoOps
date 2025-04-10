# Bürokratt's widget 

# Scope
Set up a local Buerokratt widget within Buerokratt stack

## Manual dev setup
 
Create a local project folder  ```widget```

Navigate inside created folder
Clone following repos and build images

- Clone [Ruuter](https://github.com/buerokratt/Ruuter) ```git clone https://github.com/buerokratt/Ruuter```
- Navigate to Ruuter, checkout dev branch ```git checkout dev``` and build the image `docker build -t ruuter .`
- Clone [Resql](https://github.com/buerokratt/Resql) ```git clone https://github.com/buerokratt/Resql```
- Navigate to Resql, checkout dev branch ```git checkout dev``` and build the image `docker build -t resql .`
- Clone [Chat Widget](https://github.com/buerokratt/Chat-Widget) ```git clone (https://github.com/buerokratt/Chat-Widget```
- Navigate to, checkout dev branch ```git checkout dev```build chat widget image `docker build -f Dockerfile.dev -t chat-widget .`

Run the stack with ```docker-compose up -d```

## Automatic dev setup

Create a local project folder ```widget```

Navigate inside created folder and run the set-up script
```run-widget-setup.sh```
