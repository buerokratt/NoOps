```mermaid
graph LR
  %% INFRA
  subgraph Infra[<b>Infrastruktuur</b>]
    LB[Load Balancer]
    Ingress[NGINX Ingress Controller]
    Nodes[Controller-Nodes, Worker-Nodes]
    Istio[ISTIO - mTLS]
    Calico[Calico - võrk]
    CertManager[CertManager]
    Longhorn[Longhorn - volüümid]
    Service[Kubernetes Service]
  end
  style Infra fill:#f9f,stroke:#333,stroke-width:2px

  %% ENTRY COMPONENTS
  subgraph Entry[<b>Komponendid</b>]
    Ruuter
    RuuterPrivate[Ruuter-Private]
    TIM
  end
  style Entry fill:#ccf,stroke:#333,stroke-width:2px

  %% APP COMPONENTS
  subgraph App[<b>Rakenduse Komponendid</b>]
    DataMapper
    ReSQL
    PSQLTIM[PSQL-TIM-postgresql]
    PSQLUSERS[PSQL-USERS-DB]
    Opensearch
    s3Ferry
    s3FerryPub[s3Ferry-publish]
    CronManager
    Notification
  end
  style App fill:#cff,stroke:#333,stroke-width:2px

  %% MODULES
  subgraph Modules[<b>Moodulid</b>]
    ChatWidget[Chat-Widget]
    AuthLayer[Authentication-layer]
    TrainingMod[Training-Module]
    ChatbotMod[Chatbot-Module]
    ServiceMod[Service-Module]
    AbalyticsMod[Abalytics-Module]
  end
  style Modules fill:#cfc,stroke:#333,stroke-width:2px

  %% INFRA connections
  LB --> Ingress
  Ingress --> Nodes
  Nodes <--> Istio
  Nodes <--> Calico
  Nodes <--> CertManager
  Nodes <--> Longhorn
  Nodes <--> Service
  Nodes --> Ruuter
  Nodes --> RuuterPrivate
  Nodes --> TIM

  %% ENTRY TO APP
  Ruuter --> TIM
  RuuterPrivate --> TIM

  Ruuter --> DataMapper
  Ruuter --> ReSQL
  Ruuter --> PSQLUSERS
  Ruuter --> Opensearch
  Ruuter --> s3Ferry
  Ruuter --> s3FerryPub
  Ruuter --> CronManager
  Ruuter --> Notification

  RuuterPrivate --> DataMapper
  RuuterPrivate --> ReSQL
  RuuterPrivate --> PSQLUSERS
  RuuterPrivate --> Opensearch
  RuuterPrivate --> s3Ferry
  RuuterPrivate --> s3FerryPub
  RuuterPrivate --> CronManager
  RuuterPrivate --> Notification

  TIM --> PSQLTIM

  %% MODULE RELATIONS
  Ruuter --> AuthLayer
  AuthLayer --> Ruuter
  AuthLayer --> TIM

  ChatWidget --> Ruuter

  RuuterPrivate --> TrainingMod
  RuuterPrivate --> ChatbotMod
  RuuterPrivate --> ServiceMod
  RuuterPrivate --> AbalyticsMod
