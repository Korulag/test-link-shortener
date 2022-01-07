from pydantic import BaseModel


__all__ = ['ShortLinkResponse']


class ShortLinkResponse(BaseModel):
    short_link: str
    follow_count: int
