import time
from typing import Annotated

from fastapi import FastAPI, Path, BackgroundTasks

from app.config.crowdstrike_config import Config
from app.api.v1.models import TriggerResult
from app.storage.storage_repo import StorageRepo

settings = Config.get_settings()
app = FastAPI()
storage = StorageRepo.get_storage(settings)

def start_scan(scan_meta: TriggerResult):
    print(f'Start scan of {scan_meta.host}')
    time.sleep(5)
    storage.add_scan_result(scan_meta)
    print(f'Finish scan of {scan_meta.host}')

@app.get('/scan/{host}')
def trigger_scan(background_tasks: BackgroundTasks, host=Annotated[str, Path(title='hostname to scan')]):
    trigger_result = TriggerResult(host=host)
    # last_version = storage.get_last_version(host) + 1
    background_tasks.add_task(start_scan, scan_meta=trigger_result)
    return trigger_result


@app.get('/count/{host}')
async def count(host='localhost'):
    return {"message": storage.get_last_version(host)}
