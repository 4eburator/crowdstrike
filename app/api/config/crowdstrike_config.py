from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nmap_cli: str = 'nmap -oX'
    storage_connect: str = 'lightdb://./storage'


class Config:

    @staticmethod
    def get_settings() -> Settings:
        print('INIT CONFIG')
        return Settings()
