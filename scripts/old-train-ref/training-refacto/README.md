# Flask Kubernetes Job Manager

This project is a Flask web application that manages Kubernetes jobs, specifically for training, testing, and cross-validation tasks using Rasa bots. It interacts with Kubernetes through `kubectl` commands and posts job statuses to a service called RUUTER.

## Features
- **Train Bot Endpoint**: Starts a training job using a provided job template.
- **Test Bot Endpoint**: Initiates a testing job for the bot.
- **Cross-Validation (CV) Endpoint**: Triggers cross-validation jobs for bot testing.
- **Kubernetes Integration**: Applies and deletes Kubernetes jobs using `kubectl` commands.
- **Asynchronous Status Checks**: Utilizes threads to monitor job statuses and posts updates to RUUTER.

## Requirements for script
- Python 3.x
- Flask
- PyYAML
- Requests
- Access to a Kubernetes cluster with `kubectl` configured

## Requirements for flow
- Ruuter
- Resql
- CronManager

# Local testing
## Installation for testing
1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Install dependencies:
   ```bash
   pip install flask pyyaml requests
   ```

## Usage
1. Make sure your Kubernetes context is set and accessible with `kubectl`.
2. Start the Flask server:
   ```
   python3 <script-name>.py
   ```
3. Access the endpoints using POST requests:
   - `/train-bot`: Start a bot training job.
   - `/test-bot`: Start a testing job.
   - `/test-bot-cv`: Start a cross-validation job.

## Configuration
- RUUTER status URLs are configured in the script as constants:
  ```python
  RUUTER_TRAINING_STATUS_URL = "http://localhost:8086/rasa/training-status"
  RUUTER_TEST_STATUS_URL = "http://localhost:8086/rasa/test-status"
  RUUTER_CV_STATUS_URL = "http://localhost:8086/rasa/cv-status"
  ```
- Update them as per your deployment.

# Flow Explanation
This application follows a structured flow for managing Kubernetes jobs, as demonstrated by the DSL example for the training flow. It is important to note that the Flask script itself cannot orchestrate the flow independently. Instead, the orchestration is managed by RUUTER, which controls the sequence of operations and interactions between components.

1. **Declaration**: Defines the request method (POST), content type (JSON), and accepted request body fields (`job_name` and `namespace`).
2. **Extract Request Data**: RUUTER assigns incoming request data to local variables.
3. **Get Job Template**: RUUTER makes an HTTP POST request to fetch the job template required for training.
4. **Start Training Job**: RUUTER sends a POST request to the Flask app's `/train-bot` endpoint to initiate the training job with the obtained template.
5. **Check Job Start Status**: RUUTER uses a switch-case structure to check the HTTP response:
   - If status code is 200, proceed to success response.
   - If status code is not 200, proceed to error response.
6. **Return Response**: RUUTER returns the appropriate HTTP status and message:
   - **Success**: Status 200 with "Training started."
   - **Error**: Status 500 with "Training did not start."

This flow ensures a consistent and organized approach to managing Kubernetes jobs through HTTP requests. The Flask script is responsible only for executing specific tasks as instructed by RUUTER, while RUUTER orchestrates the overall workflow.
This application follows a structured flow for managing Kubernetes jobs, as demonstrated by the DSL example for the training flow:

1. **Declaration**: Defines the request method (POST), content type (JSON), and accepted request body fields (`job_name` and `namespace`).
2. **Extract Request Data**: Assigns incoming request data to local variables.
3. **Get Job Template**: Makes an HTTP POST request to fetch the job template required for training.
4. **Start Training Job**: Sends a POST request to the Flask app's `/train-bot` endpoint to initiate the training job with the obtained template.
5. **Check Job Start Status**: Uses a switch-case structure to check the HTTP response:
   - If status code is 200, proceed to success response.
   - If status code is not 200, proceed to error response.
6. **Return Response**: Returns the appropriate HTTP status and message:
   - **Success**: Status 200 with "Training started."
   - **Error**: Status 500 with "Training did not start."

This flow ensures a consistent and organized approach to managing Kubernetes jobs through HTTP requests.

## Notes
- Ensure that `kubectl` is configured with the right context and namespace permissions.
- The job templates are expected to be in valid YAML format and passed in the request body.

## License
Dont know what to put here

