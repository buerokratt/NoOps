# NoOps

Bürokratt deployment scripts, automated tests, etc

Scripts

| Script        | Description             | Options |
| ------------- | ----------------------- | :-----: |
| `deploy-kube` | Automates K8 Deployment |  -n (NameSpaces) -p (Pods)  |

Important Notes:

- Modules Must be deployed before components in `deploy-kube`
- Notification node must be deployed before open search 
- if you didn't pass -n to `deploy-kube` then it will try to deploy all components and modules
- example `./deploy-kube.sh -n testNamespace1 -p component-byk-dmapper component-byk-ruuter module-byk-widget`
