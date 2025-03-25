#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import requests
import yaml
import threading
import time

app = Flask(__name__)

RUUTER_TRAINING_STATUS_URL = "http://localhost:8086/rasa/training-status"
RUUTER_TEST_STATUS_URL = "http://localhost:8086/rasa/test-status"
RUUTER_CV_STATUS_URL = "http://localhost:8086/rasa/cv-status"

# Helper function to run kubectl commands
def run_kubectl_apply(job_yaml: str, namespace: str) -> bool:
    try:
        if isinstance(job_yaml, bytes):  # Ensure the input is text, not bytes
            job_yaml = job_yaml.decode()
            
        apply_cmd = ["kubectl", "apply", "-f", "-", "-n", namespace]
        process = subprocess.run(apply_cmd, input=job_yaml, capture_output=True, text=True)
        
        if process.returncode != 0:
            print("Error applying job:", process.stderr)
            return False
        return True
    except Exception as e:
        print("Exception running kubectl apply:", e)
        return False

# Helper function to delete existing job in a namespace
def delete_existing_job(job_name: str, namespace: str) -> bool:
    try:
        delete_cmd = ["kubectl", "delete", "job", job_name, "-n", namespace]
        process = subprocess.run(delete_cmd, capture_output=True, text=True)
        if process.returncode == 0:
            print(f"Successfully deleted job: {job_name} in namespace: {namespace}")
        elif "NotFound" in process.stderr:
            print(f"Job not found: {job_name} in namespace {namespace}. Continuing without error.")
        else:
            print("Error deleting job:", process.stderr)
        return True
    except Exception as e:
        print("Exception deleting job:", e)
        return False

# Helper function to post job status
def post_status(url: str, status: str, job_name: str, namespace: str):
    try:
        payload = {"status": status, "job_name": job_name, "namespace": namespace}
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            print(f"Error posting status to ruuter at {url}:", response.text)
    except Exception as e:
        print(f"Error sending status to ruuter at {url}:", e)

# Common pod status and timeout logic
def check_pod_status_and_post(job_name: str, namespace: str, post_fn, timeout: int = 60):
    start_time = time.time()
    try:
        while True:
            if time.time() - start_time > timeout:
                post_fn(f"ERROR: Job '{job_name}' timed out", job_name)
                print(f"Job '{job_name}' timed out.")
                break

            get_pod_cmd = ["kubectl", "get", "pods", "-n", namespace, "-l", f"job-name={job_name}", "-o", "jsonpath={.items[*].status.phase}"]
            process = subprocess.run(get_pod_cmd, capture_output=True, text=True)

            if process.returncode == 0:
                pod_status = process.stdout.strip()
                print(f"Pod status in namespace {namespace}: {pod_status}")

                if pod_status == "Succeeded":
                    post_fn("COMPLETED", job_name, namespace)
                    break
                elif pod_status == "Failed":
                    log_cmd = ["kubectl", "logs", "-n", namespace, "-l", f"job-name={job_name}"]
                    log_process = subprocess.run(log_cmd, capture_output=True, text=True)
                    error_message = log_process.stdout.strip() if log_process.returncode == 0 else "No logs available"
                    post_fn(f"ERROR: {error_message}", job_name)
                    break
            else:
                print("Error fetching pod status.")
                post_fn("ERROR: Could not fetch pod status", job_name)
                break

            time.sleep(5)

    except Exception as e:
        print("Error checking pod status:", e)
        post_fn(f"ERROR: Exception occurred - {str(e)}", job_name)

# Dispatcher route - this will dynamically choose which job route to call
@app.route('/process-job', methods=['POST'])
def process_job():
    job_data = request.get_json()

    # Extract job type from the request (it can be 'train', 'test', or 'cv')
    job_type = job_data.get('job_type')

    if job_type == 'train':
        return train_bot()
    elif job_type == 'test':
        return test_bot()
    elif job_type == 'cv':
        return test_bot_cv()
    else:
        return jsonify({"error": "Invalid job type specified."}), 400

# Route train-bot - Handles the first step: Training
@app.route('/train-bot', methods=['POST'])
def train_bot():
    job_data = request.get_json()
    job_template = job_data.get('job')[0].get('jobTemplate')
    namespace = job_data.get('namespace', 'default')  # Default to 'default' if no namespace is provided

    if not job_template:
        return jsonify({"error": "Missing job template."}), 400

    try:
        parsed_job_template = yaml.safe_load(job_template)
    except yaml.YAMLError as e:
        return jsonify({"error": f"Invalid job template YAML: {e}"}), 400

    job_name = parsed_job_template.get('metadata', {}).get('name', 'train-bot-job')
    post_status(RUUTER_TRAINING_STATUS_URL, "IN_PROGRESS", job_name, namespace)
    delete_existing_job(job_name, namespace)

    if not run_kubectl_apply(job_template, namespace):
        post_status(RUUTER_TRAINING_STATUS_URL, "ERROR", job_name, namespace)
        return jsonify({"error": "Failed to start training job."}), 500

    post_status(RUUTER_TRAINING_STATUS_URL, "BOT_TRAINING", job_name, namespace)

    # Correct function passing: passing the update_status function
    def update_status(status, job_name, namespace):
        post_status(RUUTER_TRAINING_STATUS_URL, status, job_name, namespace)

    # Pass update_status to check_pod_status_and_post
    threading.Thread(
        target=check_pod_status_and_post, 
        args=(job_name, namespace, update_status)  # Ensure this is a function, not a string
    ).start()

    return jsonify({"message": "Training job started."}), 200

# Route test-bot - handles the second step: Testing
@app.route('/test-bot', methods=['POST'])
def test_bot():
    job_data = request.get_json()
    job_template = job_data.get('job')[0].get('jobTemplate')
    namespace = job_data.get('namespace', 'default')

    if not job_template:
        return jsonify({"error": "Missing job template."}), 400

    try:
        parsed_job_template = yaml.safe_load(job_template)
    except yaml.YAMLError as e:
        return jsonify({"error": f"Invalid job template YAML: {e}"}), 400

    job_name = parsed_job_template.get('metadata', {}).get('name', 'test-bot-job')
    post_status(RUUTER_TEST_STATUS_URL, "IN_PROGRESS", job_name, namespace)
    delete_existing_job(job_name, namespace)

    if not run_kubectl_apply(job_template, namespace):
        post_status(RUUTER_TEST_STATUS_URL, "ERROR", job_name, namespace)
        return jsonify({"error": "Failed to start testing job."}), 500

    post_status(RUUTER_TEST_STATUS_URL, "TESTING", job_name, namespace)

    def update_status(status, job_name, namespace):
        post_status(RUUTER_TEST_STATUS_URL, status, job_name, namespace)

    threading.Thread(
        target=check_pod_status_and_post, 
        args=(job_name, namespace, update_status)
    ).start()

    return jsonify({"message": "Testing job started."}), 200

# Route test-bot-cv - handles the third step: Cross validation
@app.route('/test-bot-cv', methods=['POST'])
def test_bot_cv():
    print("Received POST request on /test-bot-cv")
    job_data = request.get_json()
    job_template = job_data.get('job')[0].get('jobTemplate')
    namespace = job_data.get('namespace', 'default')

    if not job_template:
        return jsonify({"error": "Missing job template."}), 400

    try:
        parsed_job_template = yaml.safe_load(job_template)
    except yaml.YAMLError as e:
        return jsonify({"error": f"Invalid job template YAML: {e}"}), 400

    job_name = parsed_job_template.get('metadata', {}).get('name', 'cv-job')
    post_status(RUUTER_CV_STATUS_URL, "IN_PROGRESS", job_name, namespace)
    delete_existing_job(job_name, namespace)

    if not run_kubectl_apply(job_template, namespace):
        post_status(RUUTER_CV_STATUS_URL, "ERROR", job_name, namespace)
        return jsonify({"error": "Failed to start cross-validation job."}), 500

    post_status(RUUTER_CV_STATUS_URL, "CROSS_VALIDATING", job_name, namespace)

    def update_status(status, job_name, namespace):
        post_status(RUUTER_CV_STATUS_URL, status, job_name, namespace)

    threading.Thread(
        target=check_pod_status_and_post, 
        args=(job_name, namespace, update_status)
    ).start()

    return jsonify({"message": "Cross-validation job started."}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
