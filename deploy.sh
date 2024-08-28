#!/bin/bash

for cmd in git kubectl helm python3; do
    if ( ! which "$cmd" > /dev/null 2>&1 ); then
        echo "Command '$cmd' is required, but not installed! Aborting."
        exit 1
    fi
done

if [ ! -f "secrets.yaml" ]; then
    echo "Did not find secrets.yaml. Make sure you have secrets.yaml configured with correct values"
    exit 1
fi

echo "pulling Noops from https://github.com/buerokratt/NoOps"
if [ -d "NoOps" ]; then
    echo "NoOps repo already exists"
else
    git clone https://github.com/buerokratt/NoOps.git
fi

cd NoOps/helm_deploy_v2
rm secrets.yaml && cp ../../secrets.yaml .
python3 git_clone.py git.yaml
python3 libraries/install_libraries.py requirements.json
python3 secrets.py secrets.yaml
python3 deploy.py components.yaml
python3 deploy.py modules.yaml
python3 deploy.py post-deploy.yaml
cd ../../
echo "Done"
