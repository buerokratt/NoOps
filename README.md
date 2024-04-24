# NoOps

Bürokratt deployment scripts, automated tests, etc

Scripts

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
##### For example:
New Post-deployment chart `test` path `../../Kubernetes/Post-deploy/test` update script with following  
```
  test)
    helm install "$RELEASE_NAME" ../../Kubernetes/Post-deploy/test -n "$NAMESPACE"
    ;;
```  

- `./remove-kube.sh` will uninstall all the running pods under the given namespace. if the `-p` is left blank, it uninstalls all the pods in given namespace
- Scripts run deployments from `Kubernetes` folder