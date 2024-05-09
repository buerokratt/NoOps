##### Installing the charts without tarball  
I will use analytics-module and ruuter as examples  

First, create a namespace   


```
kubectl create namespace byk-test  
```
  
```
helm install analytics-module ./Modules/Analytics-Module --namespace byk-test  
```
  
```
helm install ruuter ./Components/Ruuter --namespace byk-test  
```
  
Use same command for other modules or components  

###### Explanation  
`helm install` helm command for installation  
`analytics-module` release name  
`./Modules/Analytics-Module` path to the helm charts  
`--namespace byk-test` namespace where charts will be installed  


##### Upgrading the charts without tarball  
I will use analytics-module and ruuter as examples 

  
```
helm upgrade analytics-module ./Modules/Analytics-Module --namespace byk-test  
```
  
```
helm upgrade ruuter ./Components/Ruuter --namespace byk-test  
```
  
Use same command for other modules or components  


##### Uninstalling the charts without tarball  
I will use analytics-module and ruuter as examples 

  
```
helm uninstall analytics-module --namespace byk-test  
```
  
```
helm uninstall ruuter --namespace byk-test  
```
  
Use same command for other modules or components  

#### Installing or upgrading with tarball

##### Packaging the charts  
Change the version's inside chart_versions.yml  
Run the python script  

```
python3 charts.py
```

To deploy, run a command
helm install [RELEASE_NAME] [PATH_TO_TARBALL] -n [NAMESPACE]

For example:   
```
helm install byk-widget ./charts/Widget-1.1.0.tgz -n byrokratt
```

To upgrade:  
helm upgrade [RELEASE_NAME] [PATH_TO_TARBALL] -n [NAMESPACE]

For example:

```
helm upgrade byk-widget ./charts/Widget-1.2.0.tgz -n byrokratt
```
