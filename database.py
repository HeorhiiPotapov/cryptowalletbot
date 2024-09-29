from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME
from datetime import datetime
from bson import ObjectId


class Base(object):
    """Static class for base database manipulations."""
    DATABASE = None
    CLIENT = None

    @staticmethod
    def init() -> None:
        Base.CLIENT = AsyncIOMotorClient(MONGO_URI)
        Base.DATABASE = Base.CLIENT[DB_NAME]

    @staticmethod
    async def insert(collection, data) -> None:
        await Base.DATABASE[collection].insert_one(data)

    @staticmethod
    async def find_one(collection, query) -> dict:
        result: dict = await Base.DATABASE[collection].find_one(query)
        return result

    @staticmethod
    async def find(collection, query) -> list:
        return Base.DATABASE[collection].find(query)

    @staticmethod
    async def update_one(collection, query, new_values) -> None:
        await Base.DATABASE[collection].update_one(query, new_values)

    @staticmethod
    async def update_many(collection, query, new_values) -> None:
        await Base.DATABASE[collection].update_many(query, new_values)

    @staticmethod
    async def delete_one(collection, query) -> None:
        await Base.DATABASE[collection].delete_one(query)

    @staticmethod
    async def delete_many(collection, query) -> None:
        await Base.DATABASE[collection].delete_many(query)

    @staticmethod
    async def get_all(collection) -> list:
        return await Base.DATABASE[collection].find().to_list(length=None)

    @staticmethod
    async def count(collection, query) -> int:
        return await Base.DATABASE[collection].count_documents(query)

    @staticmethod
    async def ping() -> bool:
        res = await Base.CLIENT.admin.command('ping')
        return bool(res)


class Database(Base):
    """Static class for specific database manipulations."""

    @staticmethod
    async def user_exist(id: int) -> bool:
        user = await Database.find_one('users', {'id': id})
        return user is not None

    @staticmethod
    async def user_is_submitted(id: int) -> bool:
        user = await Database.find_one('users', {'id': id})
        return user['submitted']

    @staticmethod
    async def add_user(id: int, fullname: str, username: str) -> None:
        timestamp = round(datetime.utcnow().timestamp())
        await Database.insert('users', {'id': id, 'fullname': fullname, 'username': username, 'timestamp': timestamp,
                                        'submitted': False})

    @staticmethod
    async def submit_user(id: int) -> None:
        await Database.update_one('users', {'id': id}, {'$set': {'submitted': True}})

    @staticmethod
    async def change_user_permission(id: int, permission: bool) -> list[dict]:
        await Database.update_one('users', {'id': id}, {'$set': {'submitted': permission}})
        users = await Database.get_all('users')
        return users


    @staticmethod
    async def get_all_users() -> list[dict]:
        users = await Database.get_all('users')
        return users
