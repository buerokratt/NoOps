## Architectural Guidebook for Analytics Module

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
