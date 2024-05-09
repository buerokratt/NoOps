# NoOps

#### Bürokratt deployment scripts, automated tests, etc  

#### Deploy Bürokratt on K8s using helm

##### Pre-deployment - Cloning the repo

To get the needed scripts, component and module charts, you need to clone Buerokratt-NoOps repo  

```
git clone https://github.com/buerokratt/NoOps.git
```  

Change directory  
`cd Buerokratt-NoOps`  

Change into `<git branch you are using>` branch    
`git checkout <branch name`  

To change `values.yaml's`, change directory into   
`cd Kubernetes`   
Here look `values.yaml's` under `Components/` `Modules/` `Post-deploy/` folders.   

To run the deployment scripts, change directory into  
`cd scripts/deployment`

##### Pre-deployment - changing the values    

- Every values.yaml has a `comment` to help you with changes.
- To deploy, some changes inside values.yaml 's must be done.    
  - `domain: test.buerokratt.ee` - change domain according your domain name 
  - Change the `component-databases-users-db` and `tim-postgresql` passwords. 
    - Important: your created databases passwords, must be used in values.yaml where the DB connection are marked. There is a `# Comment` behind he line to help
  - env values under module and component, change according to your domain.   
  For example   
  `REACT_APP_RUUTER_API_URL: "https://ruuter.test.buerokratt.ee/v2/public/backoffice"`   
  into  
`REACT_APP_RUUTER_API_URL: "https://ruuter.test.MYDOMAIN.ee/v2/public/backoffice"`

- Image's are up to date, currently no changing needed.  

- First-login charts, make sure to change `isikukood` accordingly, rest can remain he same
-  When adding the `login` and `id_code` values make sure that prefix `EE` is present 
- `ingress:
  certIssuerName: letsencrypt-prod` - change the certIssuerName accordingly  



##### Deployment scripts

| Script        | Description             | Options |
| ------------- | ----------------------- | :-----: |
| `deploy-kube` | Automates K8 Deployment |  -n (NameSpaces) -p (Pods)  |
| `post-deploy-kube` | Automates K8 Deployment post deployment | -n (Namespace) -r (releasename) -c (Chartname) |
| `remove-kube` | Automates K8 Deployment uninstalling | -p (Releasename)  -n (NameSpaces)  |

Important Notes:  
- Scripts run deployments from `Kubernetes` folder
- Modules Must be deployed before components in `deploy-kube`
- Notification node must be deployed before opensearch 
- if you didn't pass -n to `deploy-kube` then it will try to deploy all components and modules
- example `./deploy-kube.sh -n <namespace> -p component-byk-dmapper component-byk-ruuter module-byk-widget`
- `./remove-kube.sh` will uninstall all the running pods under the given namespace. if the `-p` is left blank, it uninstalls all the pods in given namespace
- Postdeploy chart names - `pipeline` `first-login` `dmapperv1` `byk-bot`
  ```
  bash post-deploy-kube.sh -n <namespace> -r pipeline -c pipeline
  ```
  ```
  bash post-deploy-kube.sh -n <namespace> -r first-login -c first-login
  ```
  ```
  bash post-deploy-kube.sh -n <namespace> -r byk-bot -c byk-bot
  ```
  ```
  bash post-deploy-kube.sh -n <namespace> -r dmapperv1 -c dmapperv1
  ```

- `post-deploy-kube.sh` is for deploying the standalone singular deployments, that do not fit under components or modules. They are to be run as singular k8s jobs. Currently there are 4 deployments, if more will be put in there, make appropriate changes in the script.

Example - new Post-deployment chart `test` path `../../Kubernetes/Post-deploy/test` update script with following  
```
    test)
      echo "Installing test chart"
       helm install "$RELEASE_NAME" ../../Kubernetes/Components/test -n "$NAMESPACE"
      ;;
```  
#### Enabling the sidecar for proxying networking between pods    
Pods have restricted networking. Meaning, that only `ruuter` and `ruuter-private` pods have accessibility to other pods.   
Other pods, for example `resql` should not have access to either `ruuter` or, for example `data-mapper`  
For this purpose, we use `Istio sidecar` with `Istio destination rules` (for reference, look at the `istio-setup` charts under templates folders in `components`)  
After the `Istio` has been deployed in your K8s, enable sidecar for the `namespace` you run `byrokratt` in  

```
kubectl label namespace <YOUR PROJECT NAMESPACE> istio-injection=enabled
```

Within the `deployment` charts, under `metadata` we added the following annotation
```
  annotations:
    sidecar.istio.io/inject: "true"
