## Work log to show taken architectural decisions

### pre01.trivial (2023.01.06)

1. Describe known business rules as functions
2. Implemented first use case in some way

### pre02.generic_usecase (2023.01.07)

1. Extracted Generic use case (Command pattern) to make controllers more
   similar.
2. Referencing to Interface Segregation Pattern (ISP) we suggest having
   multiple adapters for different use cases, so DTO and adapters interfaces
   moved to use case as they will be different.

### pre03.db_adapter_isp (2023.01.09)

1. Though many adapters will have similar parts we extracted them as separate
   protocol which are combined to make real adapter interface
2. Second use case added to demonstrate how to add new adapters protocols.
3. Added files for building python distributable package

### pre04.domain_services (2023.03.25)

1. Domain services implemented as classes injected in use cases. That allows to
   exclude them from use case testing
2. Domain services are not split too much to simplify current implementation
