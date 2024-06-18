import json
import subprocess
import xmltodict
from fastapi import BackgroundTasks

from app.api.v1.models import ScanSession, ScanResult, UUIDModel, ResultCode
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
        scan_session.result_code = ResultCode.success if hosts_scanner == 1 else ResultCode.fail
        scan_session.result = scan_result

        self.storage.add_scan_result(scan_session, scan_session)

    def _run_subprocess(self, cli: tuple) -> str:
        process = subprocess.Popen(cli, shell=False, stdout=subprocess.PIPE)
        full_output = ''
        while True:
            output = process.stdout.readline()
            full_output = full_output + output.decode('utf-8')
            # print(f'###> {full_output}')
            if process.poll() is not None:
                break

        rc = process.poll()
        # print(f'DONE> {rc}')
        return full_output

    def get_scan_result(self, host: str, scan_id: str) -> ScanSession:
        return self.storage.find_result(host, scan_id)

    def get_success_scan_results_meta(self, host: str) -> list[UUIDModel]:
        return self.storage.get_all_scan_ids(host, ResultCode.success)

    def get_diff_result(self, host: str, latest_uuid: UUIDModel, prev_uuid: UUIDModel) -> list[dict]:
        latest_ports = self._extract_ports_info(host, latest_uuid)
        prev_ports = self._extract_ports_info(host, prev_uuid)
        diff_ports = list()
        for port in latest_ports:
            if port not in prev_ports:
                diff_ports.append(port)
        return diff_ports

    def _extract_ports_info(self, host: str, uuid: UUIDModel):
        scan_result = self.get_scan_result(host, str(uuid.uuid))
        return json.loads(scan_result.result.nmap_output)['nmaprun']['host']['ports']['port']
