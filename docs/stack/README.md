# Bürokratt's widget 

# Scope
Set up a local Buerokratt widget within Buerokratt stack

## Dev setup

Set up the project folder locally. Clone following repos and build images

- Clone [Ruuter](https://github.com/buerokratt/Ruuter)
- Navigate to Ruuter, checkout dev branch ```git checkout dev``` and build the image `docker build -t ruuter .`
- Clone [Resql](https://github.com/buerokratt/Resql)
- Navigate to Resql, checkout dev branch ```git checkout dev``` and build the image `docker build -t resql .`
- Clone [Data Mapper](https://github.com/buerokratt/DataMapper)
- Navigate to Data Mapper, checkout dev branch ```git checkout dev``` and build the image `docker build -t data-mapper .`
- Clone [Chat Widget](https://github.com/buerokratt/Chat-Widget)
- Navigate to, checkout dev branch ```git checkout dev```build chat widget image `docker build -f Dockerfile.dev -t chat-widget .`

Run the stack with ```docker-compose up -d```
