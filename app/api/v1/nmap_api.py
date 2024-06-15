from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Path

from app.api.config.crowdstrike_config import Config
from app.api.v1.models import TriggerResult
from app.storage.storage_repo import StorageRepo

settings = Config.get_settings()
app = FastAPI()
storage = StorageRepo.get_storage(settings)


@app.get('/scan/{host}')
async def trigger_scan(host=Annotated[str, Path(title='hostname to scan')]):
    last_version = storage.get_last_version(host) + 1
    storage.add_scan_result(host)
    return TriggerResult(host=host, scan_id=last_version)
    # return {"message": f'Hello {storage.get_name(host)} World'}


@app.get('/count/{host}')
async def count(host='localhost'):
    return {"message": storage.get_last_version(host)}
