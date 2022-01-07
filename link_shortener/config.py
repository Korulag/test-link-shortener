import typing

from pydantic import BaseSettings


__all__ = ['settings']


class Settings(BaseSettings):
    dev_mode: bool = False
    db_host: str
    db_port: int = 5432
    db_name: str = 'lsh'
    db_user: str = 'postgres'
    db_password: str
    domain_name: str = 'localhost:8000'

    @property
    def database_url(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_password}@' \
               f'{self.db_host}:{self.db_port}/{self.db_name}'

    @property
    def base_url(self):
        if not self.dev_mode:
            return f'https://{self.domain_name}'
        return f'http://{self.domain_name}'


settings = Settings()
