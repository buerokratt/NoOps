## Architectural Guidebook for Analytics Module

### Purpose of the Guidebook

This guidebook serves as a comprehensive resource for developers, architects and devops involved in the development and deployment of the Analytics Module. It outlines the architectural decisions, setup procedures, configuration management, and best practices. The goal is to ensure that all team members have a clear understanding of the system and can contribute effectively to its development and maintenance.

**Objectives:**

  - To provide a clear understanding of the technological stack and architectural choices.
  - To standardize setup and deployment processes across different environments.
  - To encourage collaboration and streamline workflows among team members.
  - To facilitate onboarding of new developers by providing detailed documentation.


#### 1. Introduction
**Overview of the Analytics Module**

The Analytics Module is designed to facilitate data collection, processing, and visualization for various applications.
 It aims to provide insights into user interactions, system performance, and business metrics. By leveraging modern technologies, this module ensures scalability, maintainability, and ease of integration with existing systems.


#### 2. Technological Stack
 **Languages**
 
- **TypeScript:** TypeScript is used for its strong typing and object-oriented capabilities, which enhance code quality and maintainability.
- **SCSS:** SCSS (Sass) is utilized for styling to allow for modular and reusable CSS, making it easier to manage styles across the application.
- **JavaScript:** JavaScript serves as the foundation for client-side functionality and dynamic content manipulation.
 
 **Frameworks and Libraries**
 
- **React:** The module employs React for building user interfaces, providing a component-based architecture that promotes reusability and efficient updates.
- **Express:** Express.js is used as the web framework for handling HTTP requests and routing, ensuring a lightweight and flexible backend.
 
 **Database**
 
- **PostgreSQL:** PostgreSQL is chosen for its robustness and support for advanced features like JSONB, which is beneficial for storing complex data structures.
 
 **Containerization**
 
- **Docker:** Docker is used to create isolated environments for development, testing, and production. This ensures consistency across different setups and simplifies dependency management.
 
 **Deployment**
 
- **Kubernetes:** Kubernetes is utilized for orchestrating containerized applications, enabling automated deployment, scaling, and management of application services.
 
 **Additional Tools**
 
- **Husky:** Husky is integrated to manage Git hooks, ensuring code quality by enforcing linting and testing before commits.
- **OpenAPI:** OpenAPI specifications are used to document RESTful APIs, enabling automatic generation of API documentation and client libraries.
 
 **Rationale for Choices**
 
 Each technology was selected based on its performance, community support, and compatibility with existing tools. This stack is designed to ensure the module is scalable, maintainable, and capable of meeting the demands of modern applications.

### 3. Setup Instructions

#### Development Setup

1. **Cloning the Repository**
   - Open your terminal and run the following command to clone the repository:
     ```bash
     git clone https://gitlab.ria.ee/BYK/Analytics-Module.git
     cd Analytics-Module
     ```
   
2. **Building Necessary Images**
   - Navigate to each subdirectory and build the Docker images:
     ```bash
     # For Ruuter
     cd Ruuter
     docker build -t ruuter .

     # For Resql
     cd ../Resql
     docker build -t resql .

     # For Data Mapper
     cd ../DataMapper
     docker build -t data-mapper .

     # For TIM
     cd ../TIM
     docker build -t tim .

     # For Cron Manager
     cd ../CronManager
     docker build -t cron-manager .
     ```

3. **Running the Application Locally**
   - Ensure that you have Docker Compose installed. Run the following command to start all services:
     ```bash
     docker compose up -d
     ```
   - Once the services are running, access the application at [http://localhost:3001](http://localhost:3001).

#### Database Setup

1. **Initial Database Configuration**
   - To set up the database, run the following command:
     ```bash
     docker run --platform linux/amd64 --network=bykstack riaee/byk-users-db:liquibase20220615 --url=jdbc:postgresql://users_db:5432/byk --username=byk --password=01234 --changelog-file=./master.yml update
     ```

2. **Running Migrations**
   - To apply migrations included in the repository, execute the helper script:
     ```bash
     ./migrate.sh
     ```

3. **Creating Default Users**
   - To add a default user and bot configuration, run this command while the `users_db` container is running:
     ```bash
     docker exec users_db psql byk byk -c "INSERT INTO public.\"user\" (login,password_hash,first_name,last_name,id_code,display_name,status,created) VALUES ('EE90009999999','t','t','t','EE90009999999','t',NULL,NULL);"
     docker exec users_db psql byk byk -c "INSERT INTO public.\"configuration\" (\"key\",value) VALUES ('bot_institution_id','botname');"
     ```

#### Common Pitfalls
- Ensure Docker is running before executing any Docker commands.
- Check for any network issues if the application is not accessible at the specified URL.
- Verify that the correct permissions are set for the migration scripts.

#### Conclusion
Following these setup instructions will allow developers to run the Analytics Module locally, enabling them to contribute effectively. If any issues arise during setup, refer to the troubleshooting section or seek assistance from the team.


### 4. **Configuration Management**
Environment Variables

Configuration management is crucial for ensuring that the application behaves correctly in different environments. The following environment variables are essential for both development and production setups:

##### 1. Common Environment Variables
- REACT_APP_LOCAL: Set to true for local development. This variable enables specific features tailored for local testing.
- DATABASE_URL: The connection string for the PostgreSQL database.
```plaintext 
DATABASE_URL=jdbc:postgresql://users_db:5432/byk
```
        

- JWT_SECRET: Secret key used for signing JSON Web Tokens (JWT). Ensure this is kept secure.
- NODE_ENV: Defines the environment. Set to development or production as appropriate.

##### 2. Environment Files
- .env: Contains default environment variables for development.
- .env.dev: Used specifically for development configurations.
- .env.gui: Contains configurations for the graphical user interface.

##### Example Configuration

Here’s an example of what a typical .env file might look like:
```plaintext
    REACT_APP_LOCAL=true
    DATABASE_URL=jdbc:postgresql://users_db:5432/byk
    JWT_SECRET=your_jwt_secret
    NODE_ENV=development
```

##### Configuration for Production

For production deployments, ensure that sensitive information is not hard-coded. Use environment variables to manage configurations securely. For example:

- In Kubernetes, the `REACT_APP_MENU_JSON` variable can be configured as follows:
    ```yaml
    env:
        - name: REACT_APP_MENU_JSON
          value: "[{\"id\":\"analytics\",\"label\":{\"en\":\"Analytics\"},\"path\":\"/analytics\"}]"
    ```

##### Best Practices

- Version Control: Do not include .env files in version control. Use .gitignore to exclude them.
- Documentation: Maintain a separate documentation file (e.g., CONFIGURATION.md) that outlines the purpose of each environment variable.
- Sensitive Data: Use secret management tools (e.g., HashiCorp Vault, AWS Secrets Manager) to manage sensitive data securely.

##### Conclusion

Proper configuration management ensures that the Analytics Module operates reliably across different environments. By following these guidelines, developers can avoid common pitfalls and streamline the deployment process.

### 5. **Component Architecture**
#### Overview

The component architecture of the Analytics Module is designed to promote modularity, reusability, and separation of concerns. Each component serves a specific function within the application, allowing for easier maintenance and scalability.
Key Components

- ##### Data Mapper
    - Responsible for transforming and mapping data between the application and the database.
    - Utilizes Handlebars for templating, enabling dynamic content rendering based on user input.
    - Example modification in Server.js:
        ```javascript
            app.post('/hbs/*', (req, res) => {
                res.render(req.params[0], req.body, function(_, response) {
                    if (req.get('type') === 'csv') {
                        res.json({response});
                    } else if (req.get('type') === 'json') {
                        res.json(JSON.parse(response));
                    }
                    res.render(req.params[0], req.body);
                });
            });
        ```
- ##### User Interface Components
    - Built using React, these components manage the presentation layer of the application.
    - Components such as Header and Main Navigation are defined as external dependencies, allowing for consistent UI across different modules.
    - Example dependencies in package.json:
        ```json
        "@buerokrat-ria/header": "^0.0.1",
        "@buerokrat-ria/menu": "^0.0.1",
        "@buerokrat-ria/styles": "^0.0.1"
        ```
- ##### Analytics Services
    - Handles the collection and processing of analytics data.
    - Integrates with third-party analytics tools and APIs to provide insights into user behavior and application performance.

- ##### Authentication Module (TIM)
    - Manages user authentication and session management.
    - Requires initial login via a curl command or Postman to set cookies in the application.
    - Example curl command for login:
 
     ```plaintext
        curl -X POST -H "Content-Type: application/json" -d '{
              "login": "EE30303039914",
              "password": "OK"
            }' http://localhost:8080/analytics/auth/login
    ```
##### Interaction Between Components

- Components communicate through well-defined APIs and data contracts, ensuring that changes to one component do not adversely affect others.
- The architecture supports asynchronous data fetching, allowing the UI to remain responsive while data is being processed.

#### Best Practices

- Component Reusability: Design components to be reusable across different parts of the application, reducing code duplication.
- Separation of Concerns: Keep business logic separate from UI logic to enhance maintainability.
- Documentation: Maintain clear documentation for each component, including its purpose, usage, and any dependencies.

##### Conclusion

The component architecture of the Analytics Module is structured to facilitate collaboration among developers while ensuring a scalable and maintainable codebase. By adhering to best practices, the team can efficiently develop new features and enhancements.

## 6. **API Integration**
##### Overview

The Analytics Module interacts with various APIs to handle data retrieval, user authentication, and analytics processing. This section outlines the key APIs used, their endpoints, and how to interact with them.
##### Authentication API

- **Login Endpoint**
    - URL: /analytics/auth/login
    - Method: POST
    - Request Body:
    ```json
    {
      "login": "string",
      "password": "string"
    }
    ```

- **Response**
    - On success: Returns a JWT token and user details.
    - On failure: Returns an error message.

- **Example Curl Command**
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{
              "login": "EE30303039914",
              "password": "OK"
            }' http://localhost:8080/analytics/auth/login
    ```

- **Setting Cookies**
        After a successful login, store the JWT token as a cookie named customJwtCookie in the browser for subsequent requests.

**Data Retrieval API**

- **Get Analytics Data**
    - URL: /analytics/data
    - Method: GET
    - Query Parameters:
        - startDate: Start date for the analytics data.
        - endDate: End date for the analytics data.
    - Response:
        - Returns a JSON object containing analytics metrics.
- **Example Request**
    ```http
    GET /analytics/data?startDate=2023-01-01&endDate=2023-01-31
    ```

- **Fetch User Interactions**
    - URL: /analytics/user-interactions
    - Method: GET
    - Response:
        - Returns a list of user interactions within the specified time frame.
    - Example Request:
    ```http
    GET /analytics/user-interactions
    ```
**Error Handling**

- Ensure to handle errors gracefully in your API calls. Check for HTTP status codes and provide meaningful feedback to the user or administrator.
- Common status codes:
    - **200**: Success
    - **401**: Unauthorized (e.g., invalid token)
    - **404**: Not Found (e.g., invalid endpoint)
    - **500**: Internal Server Error

**Best Practices**

- Rate Limiting: Implement rate limiting on APIs to prevent abuse and ensure fair usage.
- Secure Endpoints: Protect sensitive endpoints with authentication and authorization checks.
- Documentation: Maintain clear API documentation using OpenAPI specifications, detailing each endpoint, request/response formats, and example usage.

**Conclusion**

Effective API integration is crucial for the functionality of the Analytics Module. By following best practices and maintaining clear documentation, developers can ensure seamless communication between components and enhance the overall user experience.

## 7. **Deployment Guidelines**
**Overview**

Deploying the Analytics Module requires careful planning to ensure that the application runs smoothly in production. This section outlines the necessary steps and best practices for deploying the module on Kubernetes and other environments.
**Pre-Deployment Checklist**
- **Environment Configuration**
    - Ensure all environment variables are set correctly for production.
    - Verify that sensitive information is managed securely.
- **Containerization**
    - Confirm that all Docker images are built and tagged appropriately.
    - Use a consistent naming convention for images to avoid confusion.
- **Testing**
    - Run automated tests to verify that the application functions as expected.
    - Conduct performance testing to ensure the application can handle expected loads.

##### Kubernetes Deployment

- **Kubernetes Configuration**
    - Create a deployment YAML file for the Analytics Module. An example configuration might look like this:
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: analytics-module
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: analytics-module
      template:
        metadata:
          labels:
            app: analytics-module
        spec:
          containers:
            - name: analytics-module
              image: registry.gitlab.ria.ee/byk/analytics-module:latest
              ports:
                - containerPort: 3001
              env:
                - name: REACT_APP_MENU_JSON
                  value: "[{\"id\":\"analytics\",\"label\":{\"en\":\"Analytics\"},\"path\":\"/analytics\"}]"
    ```
- **Service Configuration**
    - Expose the Analytics Module using a Kubernetes Service:
    ```yaml

    apiVersion: v1
    kind: Service
    metadata:
      name: analytics-service
    spec:
      type: LoadBalancer
      ports:
        - port: 80
          targetPort: 3001
      selector:
        app: analytics-module
    ```
- **Applying Configurations**
    - Deploy the configurations to your Kubernetes cluster:
    ```bash
        kubectl apply -f deployment.yaml
        kubectl apply -f service.yaml
    ```
- **Helm charts**    
    - To be ADDED


- **Monitoring and Logging**
    - Monitoring: Integrate monitoring tools like Prometheus or Grafana to track the health and performance of the application.
    - Logging: Centralize logs using tools like Elasticsearch or Fluentd for easier access and analysis. Ensure that logs are rotated and managed properly to avoid storage issues.

- **Rollback Plan**
    - Always have a rollback plan in case of deployment failures. Use Kubernetes’ built-in features to revert to previous stable versions.

- **Post-Deployment Steps**
    - **Smoke Testing**
        - Perform smoke tests to confirm that the application is functioning correctly after deployment.
    - **User Notifications**
        - Inform users of new features or changes, if applicable.
- **Performance Monitoring**
    - Continuously monitor the application’s performance and address any issues that arise.

**Conclusion**
Following these deployment guidelines will help ensure a smooth transition of the Analytics Module to production. By adhering to best practices, such as thorough testing and careful configuration management, the team can minimize downtime and enhance user satisfaction.


## 8. **Version Control and Collaboration**

**Overview**
Effective version control and collaboration practices are essential for maintaining the integrity of the Analytics Module's codebase. This section outlines the recommended Git workflow, branching strategies, and collaboration tools to facilitate teamwork.

**Git Workflow**

- **Repository Structure**
    - Repo should be forked by developer
    - Each feature or bug fix should be developed in its own branch, created from the dev branch in the fork.
    - Naming convention for branches:
        - Feature branches: NOTE to self - **Should i add this part ??**

**Committing Changes**
- Write clear and concise commit messages that describe the changes made. Follow this format:

- ***Example commit types***:
            **[Feature]**: New features
            **[Fix]**: Bug fixes
            **[Docs]**: Documentation updates
            **[Refactor]**: Refactoring the code, logic, UI, core components etc.
            **[Style]**: Style related commits 
            **[Test]**: commits regarding UI or Unit tests

**Pull Requests (PRs)**
- Once a feature or bug fix is complete, create a pull request to merge changes into the `dev` branch.
- Include a description of the changes, related issues, and any relevant context.
- Request reviews from at least one other team member before merging.


**Collaboration Tools**

- **Code Review**
    - Use code reviews to encourage constructive feedback and suggest improvements.

- **Issue Tracking using `project board`**
    - Use GitHub Issues to manage bugs, feature requests, and developments. Each issue should have a clear title and description.
    - Issues are added to the appropriate GitHub Project board to organize work by priority, status, or workflow stage
    - Assign issues to team members to clarify ownership and responsibilities.

- **Documentation**
    - Maintain up-to-date documentation in the repository, including the architectural guidebook, setup instructions, and API documentation.
    - Use Markdown for clarity and ease of editing.

**Best Practices**
- Regular Updates
- Regular deployents
- Communicate: Use team communication tools (e.g., Microsoft Teams) to discuss ongoing work and share progress.
- Celebrate Contributions: Recognize team members’ contributions to foster a positive collaborative environment.

## 9. **Troubleshooting and FAQs**
- **Common Issues and Resolutions**
    - ***Application Not Starting***
        - Symptoms: The application fails to launch, or you see error messages in the terminal.
        - Resolution:
            - Ensure Docker is running and properly configured.
            - Check for any syntax errors in your .env files.
            - Review the logs for any specific error messages using:
        ```bash
        docker-compose logs
        ```
        or
        ```bash
        kubectl -n <namespace> logs <pod>
        ```

    - ***Database Connection Issues***
        - Symptoms: Errors related to database connectivity.***
        - Resolution:
            - Verify that the database container is running and accessible.
            - Check your DATABASE_URL environment variable for correctness.
            - Ensure that the database credentials match those set in your Docker setup.

    - ***Authentication Failures***
        - Symptoms: Unable to log in or receive unauthorized errors.
        - Resolution:
            - Confirm that the correct login credentials are used.
            - Ensure that the JWT secret is correctly configured in your environment variables.
            - Check if the customJwtCookie is set after login.

    - ***API Request Failures***
        - Symptoms: HTTP errors (e.g., 404, 500) when making API calls.
        - Resolution:
            - Check the endpoint URL for typos.
            - Ensure that the server is running and accessible.
            - Review the API documentation for correct request formats.

    - ***Frontend Issues***
        - Symptoms: UI does not render as expected or displays errors in the console.
        - Resolution:
            - Check the browser console for any JavaScript errors.
            - Ensure that all required dependencies are installed by running:
        ```bash
            npm install
        ```
        - Clear browser cache and refresh the page.

#### **Frequently Asked Questions (FAQs)**

- **What should I do if I encounter a bug?**
    -  Report the bug by creating a new issue in the GitHub repository. Provide a detailed description, steps to reproduce, and any relevant screenshots or error messages. If part of the development team, raise the issue right away with any member of the eam who can control the board or help.
    
- **Where can I find the API documentation?**
    - The API documentation is maintained in the docs directory of the repository. You can also consult the OpenAPI specifications if available.


## 10. **Conclusion**
**Summary of Best Practices**
The successful development and deployment of the Analytics Module rely on adhering to best practices across various aspects of the project. Key takeaways include:

- Modular Architecture: Maintain a clean, modular architecture to promote reusability and ease of testing.
 - Comprehensive Documentation: Keep documentation up to date, covering setup, configuration, API usage, and troubleshooting to facilitate onboarding and collaboration.
- Effective Version Control: Utilize Git workflows to manage code changes, encourage collaboration through pull requests, and maintain a clear history of project evolution.
- Robust Testing: Implement automated testing to catch issues early and ensure code quality before deployment.

