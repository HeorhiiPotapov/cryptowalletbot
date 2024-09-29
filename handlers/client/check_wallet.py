from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import FSInputFile

import keyboards
import states
from database import Database
from parser import parse_address

router = Router(name=__name__)




@router.message(Command('check'))
async def start(message: Message, state: FSMContext) -> None:
    user_submitted = await Database.user_is_submitted(message.from_user.id)

    if user_submitted:
        await message.answer('Enter crypto wallet address:')
        await state.set_state(states.EnterAddress.address)
    else:
        await message.answer('😔 You are not sumbmitted. Click button to pay', reply_markup=keyboards.pay_kb())


@router.message(states.EnterAddress.address)
async def enter_address(message: Message, state: FSMContext) -> None:
    info_msg = await message.answer('⌚ Looking for data...')
    response = parse_address(message.text)
    if response:
        # await message.bot.send_message(message.from_user.id, text=response.get('main_data'))
        await message.bot.send_document(
            message.from_user.id,
            FSInputFile(response.get('filename'), response.get('filename')),
            caption=response.get('main_data')
        )
    else:
        await message.answer('Error while retrieving information, please wait and try later')
    await state.clear()
