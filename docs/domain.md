## Deseos17
### Project description

Application for wish list management with telegram bot and web ui

### Models

Blue models are to be implemented now
Gray models are planned and need to be clarified

```mermaid
flowchart LR
    User -- owns --> WishList 
    WishList -- contains --> Wish
    User --> ShareRule
    WishList --> ShareRule
    
    User -- owns --> Holiday
    User --> Calendar --> Holiday
    User --> Feed --> FeedPost --> Wish
    FeedPost --> Holiday
    User --> Relationship 
    User --> Relationship
    
    style Feed fill:#eee,stroke: #ddd
    style FeedPost fill:#eee,stroke: #ddd
    style Holiday fill:#eee,stroke: #ddd
    style Calendar fill:#eee,stroke: #ddd
    style Relationship fill:#eee,stroke: #ddd
```

### Use cases

```mermaid
flowchart LR
    Guest(((Guest)))
    User(((User)))

    Public(View public wishlist)
    AllOwnLists(View all own wishlists)
    CreateWishList(Create wishlist)
    CreateWish(CreateWish)  
    ViewOwnWishList(View own wishlist)
    ViewRecent(View recent own wishes)
    ViewSharedWishList(View shared wishlist)
    ViewAllShared(View all shared wishlists)
    Share(Share wishlist to user)
    MakePublic(Make public)
    ViewShare(View sharing settings)
    UnShare(Delete sharing)
    DeleteWish(Delete wish)
    UpdateWish(Update wish)
    DeleteWishList(Delete wishlist)    
    GetLink(Get public link)    
    
    Guest --> Login
    Guest --> Public
    User --> AllOwnLists --> ViewOwnWishList --> CreateWish
    AllOwnLists --> DeleteWishList
    AllOwnLists --> CreateWish
    AllOwnLists --> CreateWishList
    AllOwnLists --> Share
    ViewOwnWishList --> Share
    ViewOwnWishList --> MakePublic --> GetLink
    ViewOwnWishList --> DeleteWishList
    ViewOwnWishList --> DeleteWish
    ViewOwnWishList --> UpdateWish
    ViewOwnWishList --> ViewShare
    ViewShare --> UnShare
    ViewShare --> GetLink
    User --> Public
    User --> ViewRecent --> DeleteWish
    ViewRecent --> UpdateWish
    User --> CreateWishList --> ViewOwnWishList
    User --> ViewAllShared --> ViewSharedWishList
    
```
