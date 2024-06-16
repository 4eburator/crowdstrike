import datetime
import os.path
from abc import ABCMeta, abstractmethod
from urllib.parse import ParseResult

from tinydb import TinyDB

from app.api.v1.models import TriggerResult


class Storage(metaclass=ABCMeta):
    @abstractmethod
    def add_scan_result(self):
        pass

    @abstractmethod
    def get_last_version(self) -> int:
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

    def add_scan_result(self, scan_trigger: TriggerResult):
        doc = {'scan_uuid': str(scan_trigger.uuid),
               'ts': datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S'),
               'result_code': 'SUCCESS',
               'scan_result': {'hello': scan_trigger.host}}
        self._open_db(scan_trigger.host).insert(doc)

    def get_last_version(self, host: str) -> int:
        docs = self._open_db(host).all()
        return len(docs)
