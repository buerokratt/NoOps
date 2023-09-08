#### About  
Here is how to publish and pull npm repo from Github npm registry  

##### NPM publish  
Step 1
Change your project package.json - 
`"name": "@user/repo_name_you_want_to_use",`  
change the name according to github user/organization and repo name

```
 "publishConfig": {
  "registry": "https://ghcr.io/"
},
  "repository": {
  "type": "git",
  "url": "https://github.com/varmoh/cvi"
}
```
Change the registry name and repository url to reflect the repo, where package.json is.

##### NPM pull
Make sure that .npmrc has your PAT (Personalized Auth Token) in.
Log in, change @USERNAME accordingly
```
npm login --registry=https://npm.pkg.github.com --scope=@USERNAME
```

Install
```
npm install @username/repo
```
