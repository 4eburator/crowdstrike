from typing import Annotated

from fastapi import FastAPI, Path, BackgroundTasks, HTTPException

from app.config.crowdstrike_config import Config
from app.api.v1.models import ScanSession
from app.control.control_man import ControlManager

app = FastAPI()
ctrl = ControlManager(Config.get_settings())

@app.post('/scan/{host}')
async def trigger_scan(background_tasks: BackgroundTasks, host=Annotated[str, Path(title='hostname to scan')]):
    scan_session = ScanSession(host=host)
    ctrl.trigger_host_scan(scan_session=scan_session, background_tasks=background_tasks)
    return scan_session


@app.get('/scan/{host}/{uuid}')
async def get_scan(host=Annotated[str, Path(title='hostname to scan')],
                   scan_id=Annotated[str, Path(title='ID of scan')]) -> ScanSession:
    result = ctrl.get_scan_result(host, scan_id)
    if not result:
        raise HTTPException(status_code=404, detail='Scan result is not found')
    return result
