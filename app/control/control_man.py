import time
from fastapi import BackgroundTasks

from app.api.v1.models import ScanSession, ScanResult
from app.config.crowdstrike_config import Settings
from app.storage.storage_repo import StorageRepo


class ControlManager:
    def __init__(self, settings : Settings):
        super().__init__()
        self.settings = settings
        self.storage = StorageRepo.get_storage(settings)

    def trigger_host_scan(self, scan_session: ScanSession, background_tasks: BackgroundTasks):
        background_tasks.add_task(self._start_scan, scan_session = scan_session)

    def _start_scan(self, scan_session: ScanSession):
        print(f'Start scan of {scan_session.host}')
        time.sleep(5)
        scan_result = ScanResult(result_code='SUCCESS', result='all ports are open')
        scan_session.result = scan_result
        self.storage.add_scan_result(scan_session, scan_session)
        print(f'Finish scan of {scan_session.host}')
