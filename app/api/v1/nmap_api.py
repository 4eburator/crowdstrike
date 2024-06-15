from fastapi import FastAPI, Depends

from app.api.config.crowdstrike_config import Config
from app.storage.storage_repo import StorageRepo

settings = Config.get_settings()
app = FastAPI()
storage = StorageRepo.get_storage(settings)

# def read_config():
#     return storage_repo

@app.get('/')
async def root():
    return {"message": f'Hello {storage.get_name()} World'}


@app.get('/bye')
async def bye():
    return {"message": "good bye"}
