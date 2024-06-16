from urllib.parse import urlparse

from fastapi import HTTPException

from app.config.crowdstrike_config import Settings
from app.storage.storage import Storage, TinyDBStorage


class StorageRepo:
    @staticmethod
    def get_storage(settings: Settings) -> Storage:
        storage_connect_string = urlparse(settings.storage_connect)
        if 'tinydb' == storage_connect_string.scheme:
            return TinyDBStorage(storage_connect_string)
        else:
            raise HTTPException(status_code=500,
                                detail=f'Storage type {storage_connect_string.scheme} is not supported')

    # def __init__(self, settings: Settings):
    #     super().__init__()
    #     self.settings = settings
    #     print('Create Storage Repo')
    #
    # def get_name(self) -> str:
    #     storage_url = urlparse(self.settings.storage_connect)
    #     return storage_url.scheme
