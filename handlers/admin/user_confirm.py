from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import config
import keyboards
from database import Database

router = Router(name=__name__)


@router.callback_query(keyboards.UserConfirm.filter())
async def confirm_user(callback: CallbackQuery, callback_data: keyboards.UserConfirm, state: FSMContext):
    if callback_data.response:
        await Database.submit_user(callback_data.id)
        await callback.bot.send_message(callback_data.id, '✅ You was submitted and now enabled to use the bot.')
    else:
        await callback.bot.send_message(callback_data.id, '❌ You was declined and have not posibillity to use the bot.')
    await callback.message.edit_text('Answer was sent to user.')
