from datetime import datetime
from unittest.mock import Mock

import pytest

from deseos17.application.common.id_provider import IdProvider
from deseos17.application.common.uow import UoW
from deseos17.application.create_wish import NewWishDTO, DbGateway, CreateWish
from deseos17.domain.exceptions import AccessDenied
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishList, Wish, WishId, WishListId
from deseos17.domain.services.access import AccessService

NEW_WISH_ID = WishId(10000)
NEW_WISH_LIST_ID = WishListId(20000)

OWNER_ID = UserId(100)
OTHER_USER_ID = UserId(1)


@pytest.fixture()
def uow() -> UoW:
    uow_mock = Mock()
    uow_mock.commit = Mock()
    uow_mock.rollback = Mock()
    uow_mock.flush = Mock()
    return uow_mock


@pytest.fixture()
def wish_gateway() -> DbGateway:
    gateway = Mock()
    gateway.save_wish = Mock()
    gateway.get_wishlist = Mock(return_value=WishList(
        id=NEW_WISH_LIST_ID,
        owner_id=OWNER_ID,
        updated_at=datetime(2000, 12, 31),
        title="Test Wishlist",
    ))
    gateway.save_wishlist = Mock()
    gateway.get_share_rules = Mock(return_value=[])
    return gateway


@pytest.fixture()
def wish_service() -> Mock:
    service = Mock()
    service.update_wish = Mock()
    service.create_wish = Mock(return_value=Wish(
        id=NEW_WISH_ID,
        text="Test wish",
        updated_at=datetime(2000, 12, 31),
        wishlist_id=NEW_WISH_LIST_ID,
    ))
    return service


@pytest.fixture()
def owner_id_provider() -> IdProvider:
    mock_id_provider = Mock()
    mock_id_provider.get_current_user_id = Mock(return_value=OWNER_ID)
    return mock_id_provider


@pytest.fixture()
def other_id_provider() -> IdProvider:
    mock_id_provider = Mock()
    mock_id_provider.get_current_user_id = Mock(return_value=OTHER_USER_ID)
    return mock_id_provider


def test_create_wish_access(
        wish_gateway, wish_service, owner_id_provider, uow,
):
    access_service: AccessService = Mock()
    access_service.ensure_can_edit = Mock(return_value=True)
    access_service.ensure_can_create = Mock(return_value=True)

    usecase = CreateWish(
        db_gateway=wish_gateway,
        access_service=access_service,
        wish_service=wish_service,
        id_provider=owner_id_provider,
        uow=uow,
    )
    res = usecase(NewWishDTO(
        wishlist_id=NEW_WISH_LIST_ID,
        text="dto text",
    ))
    assert res == NEW_WISH_ID


def test_create_wish_no_access(
        wish_gateway, wish_service, owner_id_provider, uow,
):
    access_service: AccessService = Mock()
    access_service.ensure_can_edit = Mock(side_effect=AccessDenied)
    access_service.ensure_can_create = Mock(side_effect=AccessDenied)

    usecase = CreateWish(
        db_gateway=wish_gateway,
        access_service=access_service,
        wish_service=wish_service,
        id_provider=owner_id_provider,
        uow=uow,
    )
    with pytest.raises(AccessDenied):
        usecase(NewWishDTO(
            wishlist_id=NEW_WISH_LIST_ID,
            text="dto text",
        ))
