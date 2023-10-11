from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from deseos17.application.authenticate import LoginResultDTO
from deseos17.application.common.id_provider import IdProvider
from deseos17.presentation.interactor_factory import InteractorFactory
from . import states

start_router = Router()


@start_router.message(CommandStart())
async def start(
        message: Message,
        ioc: InteractorFactory,
        id_provider: IdProvider,
        dialog_manager: DialogManager,
) -> None:
    with ioc.authenticate(id_provider) as auth_interactor:
        auth_interactor(LoginResultDTO(
            username=message.from_user.username,
            id=message.from_user.id,
            auth_date=message.date,
            last_name=message.from_user.last_name,
            first_name=message.from_user.first_name,
            photo_url=None,
        ))
    await dialog_manager.start(
        states.GetOwnWishlists.view,
        mode=StartMode.RESET_STACK,
    )
