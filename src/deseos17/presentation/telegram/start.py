from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from .states import GetOwnWishlists

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        GetOwnWishlists.view,
        mode=StartMode.RESET_STACK,
    )
