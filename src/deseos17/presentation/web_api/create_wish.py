from fastapi import APIRouter, Depends
from typing_extensions import Annotated

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.create_wish import NewWishDTO
from deseos17.domain.models.wish import WishId
from deseos17.presentation.interactor_factory import InteractorFactory
from deseos17.presentation.web_api.dependencies.depends_stub import Stub

wish_router = APIRouter(prefix="/wishes")


@wish_router.post("/")
def create_wish(
        ioc: Annotated[InteractorFactory, Depends()],
        id_provider: Annotated[IdProvider, Depends(Stub(IdProvider))],
        data: NewWishDTO,
) -> WishId:
    with ioc.create_wish(id_provider) as create_wish_interactor:
        return create_wish_interactor(data)
