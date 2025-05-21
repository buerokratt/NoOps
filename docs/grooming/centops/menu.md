```mermaid
graph LR
    A[Dashboard Home]

    subgraph Environment
        B[Environment Selector / Filter]
    end

    subgraph SecretsManagement
        C[Secrets Management Summary]
        C --> C1[Vault Status Indicator]
        C --> C2[Secrets Count]
        C --> C3[Upcoming Rotations]
        C --> C4[Rotation Alerts]
    end

    subgraph Authentication
        D[Authentication & Token System]
        D --> D1[Active Token Count]
        D --> D2[Tokens Near Expiration]
        D --> D3[Auth Failures]
        D --> D4[Token Revocation Controls]
    end

    subgraph SecureCommunication
        E[Secure Communication Health]
        E --> E1[TLS/mTLS Status]
        E --> E2[Failed Handshakes Count]
        E --> E3[Cipher Suite Compliance]
    end

    subgraph ArtifactPipeline
        F[Artifact Delivery Pipeline Overview]
        F --> F1[Build Stage Status]
        F --> F2[Package Stage Status]
        F --> F3[Store Stage Status]
        F --> F4[Deploy Stage Status]
        F --> F5[Latest Artifact Version]
        F --> F6[Rollback Availability]
        F --> F7[Health Check Results]
    end

    subgraph Alerts
        G[Alerts and Notifications Feed]
        G --> G1[Security Alerts]
        G --> G2[Deployment Failures]
        G --> G3[Secret Rotation Failures]
        G --> G4[Communication Errors]
    end

    A --> B
    A --> C
    A --> D
    A --> E
    A --> F
    A --> G
