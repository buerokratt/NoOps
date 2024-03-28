##### Installing the charts without tarball  
I will use analytics-module as examples  

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

