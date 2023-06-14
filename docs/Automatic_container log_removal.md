#### About
Here is shown, how to remove container logs using crontab weekly

Edit file `/etc/crontab` accordingly  
```
sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*-json.log'
0  0    * * 0   root    sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*-json.log'
```
