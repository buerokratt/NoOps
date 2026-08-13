#### About  
Here is how to publish and pull an npm package from the RIA GitLab npm registry  

##### NPM publish  
Step 1
Change your project package.json - 
`"name": "@byk/repo_name_you_want_to_use",`  
the scope must match the GitLab group (`BYK`), lowercased

```
 "publishConfig": {
  "registry": "https://gitlab.ria.ee/api/v4/projects/<PROJECT_ID>/packages/npm/"
},
  "repository": {
  "type": "git",
  "url": "https://gitlab.ria.ee/BYK/cvi"
}
```
Change `<PROJECT_ID>` and the repository url to reflect the project where package.json is.
The numeric project id is on the project's main page, under the project name.

##### NPM pull
Make sure that .npmrc has your PAT (Personalized Auth Token) in. The token needs
the `read_api` scope to install, `write_registry` to publish.

```
@byk:registry=https://gitlab.ria.ee/api/v4/packages/npm/
//gitlab.ria.ee/api/v4/packages/npm/:_authToken=<YOUR_TOKEN>
```

Install
```
npm install @byk/repo
```
