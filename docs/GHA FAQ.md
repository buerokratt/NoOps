#### GIT ACTIONS

##### STEP 1 - SSH key management
Generate key-pair
ssh-keygen -t rsa -b 4096 -f ~/.ssh/***_rsa -C "buerokratt@mail.ee"
NOTE: Change the *** to reflect the repo for which you are creating the SSH for

copy private key to "Actions" (Settings/Secrets and variables/Actions) by pressing "New repository secret"
copy public key to "Deploy keys" (Settings/Deploy keys) by pressing "Add deploy key"

copy public key into deploy server (/home/ubuntu/.ssh/authorized_keys)


##### STEP 2 - Prepair server

Make sure you have the destination correct
for example: 
    in play.buerokratt.ee environment the deploy YAML is shown to push repo into /opt/etapp2/
    YAML is written, so it would create following path after it (using ruuter example) - /main/ruuter

##### STEP 3 - Build image with Git Actions, tag it using .end and push it into packages  
NOTE - This example is written using `Ruuter` repo and it triggers, when `.env` file in `dev` branch is commited to its branch
```
name: Build and publish Ruuter

on:
  push:
    branches: [ dev ]
    paths:
      - '.env'

jobs:
  PackageDeploy:
    runs-on: ubuntu-22.04

    steps:
      - uses: actions/checkout@v2

      - name: Docker Setup BuildX
        uses: docker/setup-buildx-action@v2

      - name: Load environment variables and set them
        run: |
          if [ -f .env ]; then
            export $(cat .env | grep -v '^#' | xargs)
          fi
          echo "RELEASE=$RELEASE" >> $GITHUB_ENV
          echo "VERSION=$VERSION" >> $GITHUB_ENV
          echo "BUILD=$BUILD" >> $GITHUB_ENV
          echo "FIX=$FIX" >> $GITHUB_ENV
      - name: Set repo
        run: |
           LOWER_CASE_GITHUB_REPOSITORY=$(echo $GITHUB_REPOSITORY | tr '[:upper:]' '[:lower:]')
           echo "DOCKER_TAG_CUSTOM=ghcr.io/${LOWER_CASE_GITHUB_REPOSITORY}:$RELEASE-$VERSION.$BUILD.$FIX" >> $GITHUB_ENV
      - name: Docker Build
        run: docker image build --tag $DOCKER_TAG_CUSTOM .

      - name: Log in to GitHub container registry
        run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u $ --password-stdin

      - name: Push Docker image to ghcr
        run: docker push $DOCKER_TAG_CUSTOM
```


##### STEP 4 - Deploy example YAML for pushing repo into remote server (commit trigger)

```
name: Deploy Docker Compose

on:
  push:
    branches:
      - main

jobs:
  deploy-main:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'  # Only run for the 'main' branch

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa # Change the id_rsa to mirror your GIT Secrets
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan -H ${{ secrets.MAIN_SERVER_IP }} >> ~/.ssh/known_hosts
      - name: Create directory on remote server
        run: |
          ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'mkdir -p /opt/etapp2/main'
      - name: Check if directory exists on remote server
        id: check-directory
        run: |
            ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'if [ -d "/opt/etapp2/main" ]; then echo "Directory exists"; else echo "Directory does not exist"; fi'
            ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'if [ -d "/opt/etapp2/main/ruuter" ]; then echo "Directory exists"; else echo "Directory does not exist"; fi'

      - name: Create directory on remote server
        run: |
            if [[ "${{ steps.check-directory.outputs.check-directory }}" == *"Directory does not exist"* ]]; then
            ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'mkdir -p /opt/etapp2/main'
            ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'mkdir -p /opt/etapp2/main/ruuter'
            fi

      - name: Push repository to MAIN server
        run: rsync -az --exclude='.git/' -e "ssh -i $HOME/.ssh/id_rsa" $GITHUB_WORKSPACE/ ubuntu@${{ secrets.MAIN_SERVER_IP }}:/opt/etapp2/main/

      - name: Run Docker Compose on MAIN server
        run: |
          ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'cd /opt/etapp2/main && docker-compose down && docker-compose up -d --build'
```
###### Backuping
```
      - name: Create backup of MAIN server directory # Backuping the existing folder is untested mostly (explanation below)
        run: |
          ssh -i $HOME/.ssh/id_rsa ubuntu@${{ secrets.MAIN_SERVER_IP }} 'cp -R /opt/etapp2/main /opt/etapp2/main/backup'
```
It does create a backup from repo, but when I have a backup repo already existing, it fails to create a new backup and thros errors while overwriting. Needs to be tested more.
