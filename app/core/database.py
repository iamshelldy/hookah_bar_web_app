from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


from app.core.config import get_db_url


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        name = cls.__name__.lower()
        if name.endswith('y'):
            return f"{name[:-1]}ies"
        return f"{name}s"
