from datetime import datetime

from pydantic import BaseModel


class AuditModel(BaseModel):
    id: int
    date_created: datetime
    content: str