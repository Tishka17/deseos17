from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from deseos17.application.common.dto import Pagination
from deseos17.application.common.id_provider import IdProvider
from deseos17.application.get_own_wishlists import (
    OwnWishListsResultDTO, GetOwnWishListsDTO,
)
from deseos17.domain.models.wish import WishListId
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.dependencies.depends_stub import Stub

wishlist_router = APIRouter(prefix="/wishlists")


@wishlist_router.get("/")
def get_own_wishlists(
        ioc: Annotated[InteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        limit: int = 20,
        offset: int = 0,
) -> OwnWishListsResultDTO:
    with ioc.get_own_wishlists(id_provider) as get_own_wishlists_interactor:
        return get_own_wishlists_interactor(GetOwnWishListsDTO(
            pagination=Pagination(limit=limit, offset=offset),
        ))
