from datetime import datetime
from unittest.mock import Mock

import pytest

from deseos17.domain.exceptions import AccessDenied
from deseos17.application.create_wish import NewWishDTO, DbGateway, CreateWish
from deseos17.domain.models.user_id import UserId
from deseos17.domain.models.wish import WishList, Wish, WishId, WishListId

NEW_WISH_ID = WishId(10000)
NEW_WISH_LIST_ID = WishListId(20000)


@pytest.fixture()
def db_gateway() -> DbGateway:
    gateway = Mock()
    gateway.commit = Mock()
    gateway.save_wish = Mock()
    gateway.get_wishlist = Mock(return_value=WishList(
        id=NEW_WISH_LIST_ID,
        owner_id=UserId(100),
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


def test_create_wish_access(db_gateway, wish_service):
    access_service = Mock()
    access_service.user_can_edit = Mock(return_value=True)
    access_service.user_can_create = Mock(return_value=True)

    usecase = CreateWish(
        db_gateway=db_gateway,
        access_service=access_service,
        wish_service=wish_service,
    )
    res = usecase(NewWishDTO(
        wishlist_id=NEW_WISH_LIST_ID,
        user_id=UserId(1),
        text="dto text",
    ))
    assert res == NEW_WISH_ID


def test_create_wish_no_access(db_gateway, wish_service):
    access_service = Mock()
    access_service.user_can_edit = Mock(return_value=False)
    access_service.user_can_create = Mock(return_value=False)

    usecase = CreateWish(
        db_gateway=db_gateway,
        access_service=access_service,
        wish_service=wish_service,
    )
    with pytest.raises(AccessDenied):
        usecase(NewWishDTO(
            wishlist_id=NEW_WISH_LIST_ID,
            user_id=UserId(1),
            text="dto text",
        ))
