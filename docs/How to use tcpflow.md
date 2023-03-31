#### About
Here is described on how to use network level monitoring of flow

##### How to  
Get the ID of network you want to monitor
```
docker network inspect NAME
```
Write down the docker network `name` IP to seek out the eth name
```
sudo arp -an | grep <enter IP here>
```
You should see something like `br-*************`
Use the output  
```
sudo tcpflow -c -i br-*********
```
