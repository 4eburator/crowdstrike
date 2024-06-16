from datetime import datetime
import uuid as uuid_pkg
from pydantic import BaseModel, Field, field_serializer


class UUIDModel(BaseModel):
    uuid: uuid_pkg.UUID = Field(default=uuid_pkg.uuid4(), primary_key=True, index=True, nullable=False)
    @field_serializer('uuid')
    def uuid_to_str(self, uuid1: uuid_pkg.UUID, _info) -> str:
        # return str(uuid_func())
        return str(uuid1)

class TriggerResult(UUIDModel):
    host: str
    trigger_ts: datetime = Field(default_factory=datetime.now)
    # scan_id: int
