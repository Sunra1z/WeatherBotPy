from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from config import DB_URL

engine = create_async_engine(DB_URL, echo=True)
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)