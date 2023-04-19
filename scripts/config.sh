#!/bin/bash
set -euo pipefail
IFS=$'\n\t'
organization=ORGANISATION
username=ubuntu
safe_tim_db=PASSWORD(min 6 characters)
safe_byk_db=PASSWORD(min 6 characters)
buildpath="$(pwd)"
timdb=DATABASE-VM-IP
taraid=GIVEN-FROM-TARA-ENVELOPE
tarapass=GIVEN-FROM-TARA-ENVELOPE
keytoolpass=PASSWORD(min 6 characters)
bot_url=BOT-VM-IP
training_url=TRAININGBOT-VM-IP
training_bot_dir=chatbot
SSH_KEY=PATH-TO-SSH-KEY(id_rsa)
BOT_DATA_DIR=PATH-TO-BOT-DATA
bot_name=ORGANISATION-NAME-FOR-BOT
