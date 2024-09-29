from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

import config
import keyboards
from database import Database

router = Router(name=__name__)


@router.message(CommandStart())
async def start(message: Message) -> None:
    user_exist = await Database.user_exist(message.from_user.id)
    if user_exist:
        user_submitted = await Database.user_is_submitted(message.from_user.id)
        if user_submitted:
            await message.answer('You already submitted, you can continue your work with me.')
        else:
            await message.answer('You are not sumbmitted. Click button to pay', reply_markup=keyboards.pay_kb())
    else:
        await message.answer(
            '👋 Hi. I am Insider, the first tool for advanced wallet analysis.\n At the moment, access is private, to pay, click next.',
            reply_markup=keyboards.pay_kb())
        await Database.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)


@router.callback_query(F.data == 'to_payment')
async def to_payment(callback: CallbackQuery):
    await callback.message.edit_text(f'Please, make transaction by this details:\n\n{config.CRYPTO_WALLET}')
    await callback.bot.send_message(chat_id=config.ADMIN_ID,
                                    text=f'Submit user? \nID:{callback.from_user.id}\nUsername:{callback.from_user.username}\nFullname:{callback.from_user.full_name}',
                                    reply_markup=keyboards.confirm_user_kb(callback.from_user.id))
