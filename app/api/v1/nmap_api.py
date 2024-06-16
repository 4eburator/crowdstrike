import time
from typing import Annotated

from fastapi import FastAPI, Path, BackgroundTasks

from app.config.crowdstrike_config import Config
from app.api.v1.models import ScanSession
from app.control.control_man import ControlManager
from app.storage.storage_repo import StorageRepo

# settings = Config.get_settings()
app = FastAPI()
ctrl = ControlManager(Config.get_settings())
# storage = StorageRepo.get_storage(settings)

# def start_scan(scan_meta: TriggerResult):
#     print(f'Start scan of {scan_meta.host}')
#     time.sleep(5)
#     storage.add_scan_result(scan_meta)
#     print(f'Finish scan of {scan_meta.host}')

@app.get('/scan/{host}')
async def trigger_scan(background_tasks: BackgroundTasks, host=Annotated[str, Path(title='hostname to scan')]):
    scan_session = ScanSession(host=host)
    ctrl.trigger_host_scan(scan_session=scan_session, background_tasks=background_tasks)
    return scan_session


# @app.get('/count/{host}')
# async def count(host='localhost'):
#     return {"message": storage.get_last_version(host)}
