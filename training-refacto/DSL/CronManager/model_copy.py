#!/usr/bin/env python3
import requests
import json
import os
from datetime import datetime
import sys

# Functions

def get_latest_model(directory, extensions):
    files = [
        os.path.join(directory, f) 
        for f in os.listdir(directory) 
        if os.path.isfile(os.path.join(directory, f)) and any(f.endswith(ext) for ext in extensions)
    ]
    
    if not files:
        return None
    
    latest_file = max(files, key=os.path.getmtime)  # Get the most recently modified file
    return latest_file

# Configuration Variables
pvc_mount_path = './mock-test'  # PVC mount path in the K8s job
s3_ferry_train = 'http://localhost:3005'
training_ruuter = 'http://localhost:8086'
valid_extensions = ['.tar.gz', '.txt']  # Add other extensions if needed

# Execution Flow
if __name__ == "__main__":
    try:
        latest_model_path = get_latest_model(pvc_mount_path, valid_extensions)
        if not latest_model_path:
            response = {"status": "failure", "message": "No Rasa models found in the PVC directory."}
            print(json.dumps(response))
            sys.exit(1)
        
        latest_model_filename = os.path.basename(latest_model_path)
        
        copy_file_body_dto = {
            "destinationFilePath": latest_model_filename,
            "destinationStorageType": "S3",
            "sourceFilePath": latest_model_filename,
            "sourceStorageType": "FS"
        }

        copy_file_response = requests.post(
            f"{s3_ferry_train}/v1/files/copy",
            headers={"Content-Type": "application/json"},
            data=json.dumps(copy_file_body_dto)
        )

        if copy_file_response.status_code != 201:
            error_res = requests.get(f"{training_ruuter}/rasa/model/add-new-model-error")
            response = {
                "status": "failure", 
                "message": f"Copying file from PVC to S3 failed with status code {copy_file_response.status_code}",
                "error": error_res.text
            }
            print(json.dumps(response))
            sys.exit(1)
        
        # Notify RUUTER about the filename before deletion
        notify_before_delete_body = {
            "status": "info",
            "model": latest_model_filename,
            "message": "Model successfully copied to S3, pending deletion from PVC."
        }

        notify_before_delete_response = requests.post(
            f"{training_ruuter}/rasa/model-before-delete",
            headers={"Content-Type": "application/json"},
            data=json.dumps(notify_before_delete_body)
        )

        if notify_before_delete_response.status_code != 200:
            response = {"status": "failure", "message": "Failed to notify RUUTER before deletion"}
            print(json.dumps(response))
            sys.exit(1)

        cv_status_body_dto = {
            "status": "success",
            "model": latest_model_filename,
            "message": "Model successfully moved to S3 and original deleted from PVC."
        }

        cv_status_response = requests.post(
            f"{training_ruuter}/rasa/model-moved",
            headers={"Content-Type": "application/json"},
            data=json.dumps(cv_status_body_dto)
        )

        if cv_status_response.status_code != 200:
            response = {"status": "failure", "message": "Failed to notify RUUTER"}
            print(json.dumps(response))
            sys.exit(1)
        
        # Proceed with deletion
        try:
            os.remove(latest_model_path)
        except Exception as e:
            response = {"status": "failure", "message": f"Failed to delete original model: {e}"}
            print(json.dumps(response))
            sys.exit(1)

        response = {"status": "success", "message": "All steps completed successfully."}
        print(json.dumps(response))
        sys.exit(0)

    except Exception as e:
        response = {"status": "failure", "message": f"Unexpected error: {str(e)}"}
        print(json.dumps(response))
        sys.exit(1)
