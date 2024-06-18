import datetime
import os.path
from abc import ABCMeta, abstractmethod
from urllib.parse import ParseResult

from tinydb import TinyDB, Query

from app.api.v1.models import ScanSession, ScanResult, UUIDModel, ResultCode


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def add_scan_result(self, scan_session: ScanSession, result: ScanResult):
        pass

    @abstractmethod
    def find_result(self, host: str, scan_id) -> ScanSession:
        pass

    @abstractmethod
    def get_all_scan_ids(self, host: str, result_status: ResultCode) -> list[UUIDModel]:
        pass


class TinyDBStorage(Storage):

    def __init__(self, connection_details: ParseResult, **kwargs):
        super().__init__(**kwargs)
        self.storage_path = connection_details.path.strip('/')
        print(f'TinyDBStorage path: {self.storage_path}')
        os.makedirs(self.storage_path, exist_ok=True)

    def _open_db(self, host):
        db_path = os.path.join(self.storage_path, f'{host}.json')
        return TinyDB(db_path)

    def add_scan_result(self, scan_session: ScanSession, result: ScanResult):
        self._open_db(scan_session.host).insert(result.model_dump())

    def find_result(self, host: str, scan_id: str) -> ScanSession:
        query = Query()
        results = self._open_db(host).search(query.uuid == scan_id)
        return None if len(results) == 0 else ScanSession(**results[-1])

    def get_all_scan_ids(self, host: str, result_status: ResultCode) -> list[UUIDModel]:
        rows = self._open_db(host).all()
        return [UUIDModel(**row) for row in rows
                if 'uuid' in row and result_status == row.get('result_code')]
