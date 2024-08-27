# Helm deployment v2

### How to run as a test 

#### Requirements:  

#### Minikube requirements
To run it on your local K8s cluster, a simple `minikube` is sufficent, you can find how to run it here:  
https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download

To install ` kubectl` (this is optional if it not there by default)

```
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```
```
chmod +x kubectl
```
```
sudo mv kubectl /usr/local/bin/
```

To install `helm` (this is optional if it not there by default)

```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

To install `iscsi` (not optional without this longhorn will fail)
```
minikube ssh
```
```
sudo apt-get update
```
```
sudo apt-get install -y open-iscsi
```
```
exit
```

To install `longhorn`  
```
helm repo add longhorn https://charts.longhorn.io
```
```
helm repo update
```
```
kubectl create namespace longhorn-system
```
```
helm install longhorn longhorn/longhorn --namespace longhorn-system
```
#### Python requirements  

`Python3, pip`  

Needed libraries:  

`pyyaml`  

Consult [this part](#Python-libraries) of readme, if you need to install libraries


## IMPORTANT  
To run this test, clone this repo:  
```
git clone https://github.com/buerokratt/NoOps.git
```
then  
```
cd NoOps/helm_deploy_v2

```

#### Cloning the  `No-Ops` repo
To run Buerokratt deployment clone the `No-Ops` repo where the Helm charts are:

```
python3 git_clone.py git.yaml
```
You have now cloned Buerokratt helm charts, continue with testing the deployment pipeline(s)
## Helm installation using python 


#### Python libraries  

To install use `libraries/install_libraries.py`   

```
python3 libraries/install_libraries.py requirements.json
```

This script can be used in general also to install libraries quickly and keep eye on, what has been installed.  

Use `requirements.json` for adding the libraries you need to install.

#### Preparations 

#### Changing `secrets`

Modify the secrets.yaml to give values to your secrets in values.yaml files.  
Run the script  

```
python3 secrets.py secrets.yaml
```

##### Deployment
To deploy all, run 

```
python3 deploy.py components.yaml
```

This will deploy all components in a namespace described in `components.yaml`. Same logic goes also with `modules.yaml` and `post-deploy.yaml`


To deploy only certain components or modules add the release name, 

example:

```
python3 deploy.py components.yaml component-byk-ruuter
```
or
```
python3 deploy.py modules.yaml module-byk-widget
```


##### Post deployment

```
python3 deploy.py post-deploy.yaml
```

##### Deleting deployments

To delete, run a script `uninstall.py`
Depending on directions, you can uninstall all or certain deployments
for example


```
python3 uninstall.py components.yaml
```
This will delete all components in a namespace described in `components.yaml`. Same logic goes also with `modules.yaml` and `post-deploy.yaml`

```
python3 uninstall.py components.yaml component-byk-ruuter
```

This will delete one component in a namespace described in `components.yaml`. Same logic goes also with `modules.yaml` and `post-deploy.yaml`

Note: You can add as many components/modules etc as you need to uninstall.

```
python3 uninstall.py components.yaml component-byk-ruuter component-byk-resql component-byk-xtr
```


#### Things to look out for

When updating the info inside components.yaml, modules.yaml, post-deploy.yaml follow the yaml structure very strictly.  
for example:

```
deployments:
  - name: test
    chart_path: ./
    namespace: buerokratt
  - name: test2
    chart_path: ./
    namespace: buerokratt
```

## Current issues
Currently no issues. If you find any, let me know.

## To do
 - Separating variabls into two files,for current test they are in one but they should be 2 different "configure" files
 - Add a possibility to use 2 config files within one deploy, currently script supports one config file at a time
