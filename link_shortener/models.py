import typing

import sqlalchemy
from pydantic import BaseModel

from link_shortener.database import Base


class ShortLink(Base):
    __tablename__ = 'short_links'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    link_id = sqlalchemy.Column(sqlalchemy.String(16), unique=True,
                                nullable=False)
    initial_link = sqlalchemy.Column(sqlalchemy.TEXT, unique=True,
                                     nullable=False)
    follow_count = sqlalchemy.Column(sqlalchemy.Integer, default=0,
                                     nullable=False)
