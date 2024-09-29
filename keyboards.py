import math
from http.client import responses

from aiogram.filters.callback_data import CallbackData
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def pay_kb():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='💲 Pay',
                             callback_data='to_payment')
    ]])
    return keyboard


class UserConfirm(CallbackData, prefix='userconfirm'):
    id: int
    response: bool


class UserPermission(CallbackData, prefix='userpermission'):
    id: int
    submitted: bool
    page: int


class ChangePage(CallbackData, prefix='changepage'):
    current: int
    forward: bool


def confirm_user_kb(user_id: str):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text='✅ Confirm', callback_data=UserConfirm(id=user_id, response=True).pack()),
        InlineKeyboardButton(text='❌ Decline', callback_data=UserConfirm(id=user_id, response=False).pack())
    ]])
    return keyboard


def adminpanel_kb(users: list[dict], current_page: int):
    builder = InlineKeyboardBuilder()
    for user in users[current_page * 10:(current_page * 10) + 10]:
        builder.row(
            InlineKeyboardButton(
                text=f'{user["id"]}',
                callback_data='userid'
            ),
            InlineKeyboardButton(
                text=f'{user["fullname"]}',
                callback_data='userfullname'
            ),
            InlineKeyboardButton(
                text=f'{user["username"]}',
                callback_data='userusername'
            ),
            InlineKeyboardButton(
                text=f'🛑 Block user' if user['submitted'] else '✅ Unblock user',
                callback_data=UserPermission(id=user['id'],
                                             submitted=user['submitted'],
                                             page=current_page).pack()
            )
        )

    builder.row(
        InlineKeyboardButton(
            text=f'⬅️',
            callback_data=ChangePage(current=current_page, forward=False).pack()
        ),
        InlineKeyboardButton(
            text=f"{current_page + 1}/{math.ceil(len(users) / 10)}",
            callback_data='currentpage'
        ),
        InlineKeyboardButton(
            text=f'➡️',
            callback_data=ChangePage(current=current_page, forward=True).pack()
        )
    )
    return builder.as_markup()
