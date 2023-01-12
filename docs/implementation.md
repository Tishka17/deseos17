### Implementation details

```mermaid
flowchart LR
    style Frameworks fill:#cfefff,stroke:#bcd
    subgraph Frameworks
        FastApi
        AiogramDialog
    end 
    style Adapters fill:#dfffdf,stroke:#bdb
    subgraph Adapters
        style TelegramApp fill:#eff,stroke:#cec
        subgraph TelegramApp
            ClickHandler
            DataGetter
        end
        
        style WebApp fill:#eff,stroke:#cec
        subgraph WebApp
            ViewFunction
        end
        
        style DatabaseGateway fill:#ffe,stroke:#cec
        subgraph DatabaseGateway
            SqlalchemyGatewayImpl
        end
    end
    
    style Application fill:#fdd,stroke:#dbb
    subgraph Application
        style UseCases fill:#fee,stroke:#fcc
        subgraph UseCases
            WriteUseCase
            ReadUseCase
        end
        style Ports fill:#fee,stroke:#fcc
        subgraph Ports
            WriteDbGateway
            ReadDbGateway
        end
    end
    
    style Domain fill:#ffc,stroke:#ddb
    subgraph Domain
        DomainModel
        style Services fill:#ffe,stroke:#eec
        subgraph Services
            PermissionsService
            ModelUpdateService
        end
    end
    
    User --> FastApi
    FastApi --> ViewFunction
    ViewFunction --> ReadUseCase
    
    User --> AiogramDialog
    AiogramDialog --> ClickHandler
    AiogramDialog --> DataGetter
    
    ClickHandler --> WriteUseCase
    DataGetter --> ReadUseCase
    WriteUseCase --> WriteDbGateway
    ReadUseCase --> ReadDbGateway
    WriteUseCase --> DomainModel
    ReadUseCase --> DomainModel
    WriteDbGateway --> DomainModel
    ReadDbGateway --> DomainModel
    
    SqlalchemyGatewayImpl -- implements --> WriteDbGateway
    SqlalchemyGatewayImpl -- implements --> ReadDbGateway
    
    ReadUseCase --> PermissionsService
    WriteUseCase --> PermissionsService
    WriteUseCase --> ModelUpdateService
```
