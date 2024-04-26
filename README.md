# NoOps

#### Bürokratt deployment scripts, automated tests, etc  

#### Deploying Bürokratt on K8s using helm

##### Pre-deployment    

- Every values.yam has a `comment` to help you with changes.
- To deploy, some changes inside values.yaml 's must be done.    
  - `domain: test.buerokratt.ee` - change domain accordingly 
  - Change the `component-databases-users-db` and `tim-postgresql` passwords. ##### Important: your created databases passords, must be used in values.yaml where the DB connection are marked. There is a `# Comment` behind he line to help
  - env values under module and component, change according to your domain.   
  For example   
  `REACT_APP_RUUTER_API_URL: "https://ruuter.test.buerokratt.ee/v2/public/backoffice"`   
  into `REACT_APP_RUUTER_API_URL: "https://ruuter.test.MYDOMAIN.ee/v2/public/backoffice"`

- Image's are up to date, currently no changing needed.  

- First-login charts, make sure to change `isikukood` accordingly, rest can remain he same
-  When adding the `login` and `id_code` values make sure that prefix `EE` is present 
- `ingress:
  certIssuerName: letsencrypt-prod` - change the certIssuerName accordingly 



##### Deployment scripts

| Script        | Description             | Options |
| ------------- | ----------------------- | :-----: |
| `deploy-kube` | Automates K8 Deployment |  -n (NameSpaces) -p (Pods)  |
| `post-deploy-kube` | Automates K8 Deployment post deployment | -n (Namespace) -r (releasename) -c (Chartname) -c (Chartname) |
| `remove-kube` | Automates K8 Deployment uninstalling | -p (Releasename)  -n (NameSpaces)  |

Important Notes:

- Modules Must be deployed before components in `deploy-kube`
- Notification node must be deployed before open search 
- if you didn't pass -n to `deploy-kube` then it will try to deploy all components and modules
- example `./deploy-kube.sh -n testNamespace1 -p component-byk-dmapper component-byk-ruuter module-byk-widget`
- `post-deploy-kube.sh` is for deploying the standalone singular deployments, that do not fit under components or modules. They are to be run as singular k8s jobs. Currently there are 3 deployments, if more will be put in there, make appropriate changes in the script.
- Postdeploy chart names - `pipeline` `first-login` `dmapperv1` `byk-bot` When running the post-deploy script, make sure to add `-c` infront of every chart you want to deploy

##### For example:
New Post-deployment chart `test` path `../../Kubernetes/Post-deploy/test` update script with following  
```
  test)
    helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/test -n "$NAMESPACE"
    ;;
```  

- `./remove-kube.sh` will uninstall all the running pods under the given namespace. if the `-p` is left blank, it uninstalls all the pods in given namespace
- Scripts run deployments from `Kubernetes` folder

