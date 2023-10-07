## Work log to show taken architectural decisions

### [pre01.trivial](../../../tree/pre01.trivial) (2023.01.06)

1. Describe known business rules as functions
2. Implemented first use case in some way

### [pre02.generic_usecase](../../../tree/pre02.generic_usecase) (2023.01.07)

1. Extracted Generic use case (Command pattern) to make controllers more
   similar.
2. Referencing to Interface Segregation Pattern (ISP) we suggest having
   multiple adapters for different use cases, so DTO and adapters interfaces
   moved to use case as they will be different.

### [pre03.db_adapter_isp](../../../tree/pre03.db_adapter_isp) (2023.01.09)

1. Though many adapters will have similar parts we extracted them as separate
   protocol which are combined to make real adapter interface
2. Second use case added to demonstrate how to add new adapters protocols.
3. Added files for building python distributable package

### [pre04.domain_services](../../../tree/pre04.domain_services) (2023.03.25)

1. Domain services implemented as classes injected in use cases. That allows to
   exclude them from use case testing
2. Domain services are not split too much to simplify current implementation

### [pre05.domain_errors](../../../tree/pre05.domain_errors) (2023.04.05)

1. Access related exceptions moved to domain layer. So no need to do same
   raises in all use cases

### [pre05.presentation](../../../tree/pre05.presentation) (2023.05.21)

1. Created layout for interface layer. It is split into 2 packages:
    * presentation (primary adapters in hexagonal architecture) here will be
      all related to application entrypoints: controllers and presenters.
      Actually we have two ways of interacting with our application:
        * web api (REST-like). It is going to be implemented using FastApi.
        * Telegram bot. It will use aiogram-dialogs
    * adapters. We will put here data access objects and clients for external
      APIs
2. Created simple telegram dialog to test how DI can be implemented
    * Use case interactors are created inside controllers by calling factory
      methods
    * Single factory is used for creating all use case interactors
    * Factory is injected by passing it to a dispatcher.
    * We are going to release interactor resources by using factory as a
      context manager
3. Created simple fastapi route to provide same functiontality:
    * Interactor Factory is injected using Depends
    * Interactors are created by calling factory methods as it is done in
      telegram bot
    * Pydantic schema is created to parse user data. It is slightly different
      from DTO as UserId in provided separately
    * Authentication currently is planned to be done in presentation level
3. Stub db gateway and runnable main added

### pre06.cleanup

1. Renamed `UseCase` classes to `Interactor` so the naming is more strict
2. Simplified dirs structure of application and presentation layer. Removed redundant packages.