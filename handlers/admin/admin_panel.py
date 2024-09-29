from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import config
import keyboards
from database import Database

router = Router(name=__name__)


@router.message(Command('admin'), F.from_user.id == int(config.ADMIN_ID))
async def adminpanel(message: Message):
    users = await Database.get_all_users()
    await message.answer('Users:', reply_markup=keyboards.adminpanel_kb(users, 0))


@router.callback_query(keyboards.ChangePage.filter())
async def navigation(callback: CallbackQuery, callback_data: keyboards.ChangePage):
    users = await Database.get_all_users()
    await callback.message.edit_text('Users:', reply_markup=keyboards.adminpanel_kb(users,
                                                                                    callback_data.current + 1 if callback_data.forward else callback_data.current - 1))


@router.callback_query(keyboards.UserPermission.filter())
async def user_block_unblock(callback: CallbackQuery, callback_data: keyboards.UserPermission):
    users = await Database.change_user_permission(callback_data.id, not callback_data.submitted)
    await callback.message.edit_text(f'User with id {callback_data.id} was updated:', reply_markup=keyboards.adminpanel_kb(users, callback_data.page))
