from fastapi import FastAPI, Depends

from app.api.config.crowdstrike_config import Config
from app.storage.storage import StorageRepo

settings = Config.get_settings()
app = FastAPI()
storage_repo = StorageRepo(settings)

def read_config():
    return storage_repo

@app.get('/')
async def root(config: StorageRepo = Depends(read_config)):
    return {"message": f'Hello {config.get_name()} World'}


@app.get('/bye')
async def bye():
    return {"message": "good bye"}
