#### About
Here is shown, how to remove container logs using crontab weekly (thursday midnight)

Edit file `/etc/crontab` accordingly  
```
0  0    * * 4   root    sudo sh -c 'truncate -s 0 /var/lib/docker/containers/*/*-json.log'
```
