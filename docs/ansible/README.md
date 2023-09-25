#### About  
Here are ansible playbooks to control remote servers (currently dev and test)

##### Pre-work  
Edit the `inventory.yml` to reflect your project  

##### How to run all the playbooks automatically  
If you have more then one playbook and wish to rn them in order -   
Ansible machine should have `python3`  
Edit the `playbok.py`   
Line 18 - `playbooks = ["resources.yml"]` Add the playbooks you created inside the brackets separated with a ","

Run the python script  
```
python3 playbooks.py
