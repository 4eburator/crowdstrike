import json
import subprocess
import time
import xmltodict
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
        nmap_tool_cli = (self.settings.nmap_cli + scan_session.host).split()
        nmap_xml_output = self._run_subprocess(nmap_tool_cli)
        nmap_json_output = xmltodict.parse(nmap_xml_output)
        nmap_str_output = json.dumps(nmap_json_output)

        hosts_scanner = int(nmap_json_output['nmaprun']['runstats']['hosts']['@up'])

        scan_result = ScanResult(nmap_output=nmap_str_output)
        scan_session.result_code = 'SUCCESS' if hosts_scanner == 1 else 'FAILED'
        scan_session.result = scan_result

        self.storage.add_scan_result(scan_session, scan_session)

    def _run_subprocess(self, cli: tuple) -> str:
        process = subprocess.Popen(cli, shell=False, stdout=subprocess.PIPE)
        full_output = ''
        while True:
            output = process.stdout.readline()
            full_output = full_output + output.decode('utf-8')
            if process.poll() is not None:
                break

        rc = process.poll()
        return full_output

    def get_scan_result(self, host: str, scan_id: str) -> ScanSession:
        return self.storage.find_result(host, scan_id)