from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nmap_cli: str = 'nmap -p- -oX - '
    storage_connect: str = 'tinydb://./storage'


class Config:

    @staticmethod
    def get_settings() -> Settings:
        print('INIT CONFIG')
        return Settings()
