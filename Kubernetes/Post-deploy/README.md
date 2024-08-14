#### INFO  

Here are charts, that should be run separately from modules or components.  
For example - ./pipeline deployent should be run only when the Training-Module is up and ready

To run is similar to others - 

```
helm install <RELEASE-NAME> ./Post-deploy/pipeline/ -n <NAMESPACE>
```

Replace he RELEASE-NAME and NAMESPACE with the correct valus

With other post-deloy charts, replace the folder where charts are in.