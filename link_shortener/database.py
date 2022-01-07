from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from link_shortener.config import settings


__all__ = ['Base', 'Session', 'engine']


engine = create_async_engine(settings.database_url, poolclass=NullPool)
Base = declarative_base()
Session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)
