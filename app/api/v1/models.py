from datetime import datetime

from pydantic import BaseModel, Field


class TriggerResult(BaseModel):
    host: str
    trigger_ts: datetime = Field(default_factory=datetime.now)
    scan_id: int
