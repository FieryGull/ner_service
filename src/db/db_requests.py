from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import ClauseElement

from src.core.security import get_password_hash
from src.db import Base
from src.db.models import User, Report
from src.settings import ENGINE


class SingletonMeta(type):
    """
    Singleton Metaclass
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBManager(metaclass=SingletonMeta):
    connection = None

    @classmethod
    def connect(cls):
        if cls.connection is None:
            cls.connection = AsyncSession(ENGINE, expire_on_commit=False)
        return cls.connection

    @classmethod
    def disconnect(cls):
        if cls.connection is not None:
            cls.connection.close_all()


class DBCommands:
    def __init__(self):
        self.pool = DBManager.connect()

    @staticmethod
    async def create_tables():
        """
        Async create tables

        :return: None
        """
        async with ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def drop_tables():
        """
        Async drop all tables

        :return: None
        """
        async with ENGINE.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

    async def get(self, model, **kwargs):
        """
        Get instance from db by db model and attributes

        :param model: DB model
        :param kwargs: instance's attributes
        :return: instance from DB if found, else - None
        """
        instance = await self.pool.execute(select(model).filter_by(**kwargs))
        result = instance.scalars().first()

        return result or None

    async def get_all(self, model, **kwargs):
        """
        Get all instances from db by db model and attributes condition

        :param model: DB model
        :param kwargs: instance's attributes
        :return: list of instances from DB if found, else - None
        """
        instance = await self.pool.execute(select(model).filter_by(**kwargs))
        result = instance.scalars().all()
        return result or None

    async def get_or_create(self, model, **kwargs):
        """
        Get or create(if not exist)+create instance by db-model and attributes

        :param model: DB model
        :param kwargs: instance's attributes
        :return: instance from DB, bool flag of creation
        """
        instance = await self.get(model, **kwargs)
        if instance:
            return instance, False
        else:
            params = dict((k, v) for k, v in kwargs.items() if not isinstance(v, ClauseElement))
            instance = model(**params)
            self.pool.add(instance)
            await self.pool.commit()
            return instance, True

    async def get_or_create_user(self, email: str, password: str) -> Tuple[User, bool]:
        """
        Get or create(if not exist) user instance

        :param email: User email
        :param password: User password
        :return: User instance from DB, bool flag of creation
        """
        if user := await self.get(User, email=email):
            return user, False

        user_entity = User(
            email=email,
            hashed_password=get_password_hash(password)
        )
        self.pool.add(user_entity)
        await self.pool.commit()
        return user_entity, True

    async def create_report(self, name: str, doc: bytes, user_id: str, id_: str) -> Report:
        report, _ = await self.get_or_create(Report,
                                             id=id_,
                                             user_id=user_id,
                                             doc=doc,
                                             name=name
                                             )
        return report
