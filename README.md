# NoOps

Bürokratt deployment scripts, automated tests, etc

Scripts

| Script        | Description             | Options |
| ------------- | ----------------------- | :-----: |
| `deploy-kube` | Automates K8 Deployment |  -n (NameSpaces) -p (Pods)  |
| `post-deploy-kube` | Automates K8 Deployment post deployment | -r (Releasename)  -n (NameSpaces)  |
| `remove-kube` | Automates K8 Deployment uninstalling | -p (Releasename)  -n (NameSpaces)  |

Important Notes:

- Modules Must be deployed before components in `deploy-kube`
- Notification node must be deployed before open search 
- if you didn't pass -n to `deploy-kube` then it will try to deploy all components and modules
- example `./deploy-kube.sh -n testNamespace1 -p component-byk-dmapper component-byk-ruuter module-byk-widget`
- `post-deploy-kube.sh` is for deploying the standalone singular deployments, that do not fit under components or modules. They are to be run as singular k8s jobs.
- `./remove-kube.sh` will uninstall all the running pods under the given namespace. if the `-p` is left blank, it uninstalls all the pods in given namespace
- Scripts have to be run from `Kubernetes` folder