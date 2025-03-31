#!/bin/bash
echo $1

if [[ $1 == *component_bot_image_version* ]]; then
  sed -i "s|component_bot_image_version=[^ ]*|$1|g" MasterSecrets.env
else
  echo "did not get input"

fi

echo done
