from datetime import datetime
import uuid as uuid_pkg
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer


class UUIDModel(BaseModel):
    uuid: uuid_pkg.UUID = Field(default=uuid_pkg.uuid4(), primary_key=True, index=True, nullable=False)
    @field_serializer('uuid')
    def uuid_to_str(self, uuid1: uuid_pkg.UUID, _info) -> str:
        return str(uuid1)

class ScanResult(BaseModel):
    nmap_output: str

class ResultCode(str, Enum):
    ok = 'OK'
    success = 'SUCCESS'
    fail = 'FAIL'

class ScanSession(UUIDModel):
    host: str
    trigger_ts: datetime = Field(default_factory=datetime.now)
    result_code: ResultCode = ResultCode.ok
    result: Optional[ScanResult] = ScanResult(nmap_output='')

    @field_serializer('trigger_ts')
    def ts_to_str(self, ts: datetime, _info) -> str:
        # return ts.strftime('%d/%m/%Y, %H:%M:%S')
        return str(ts)
