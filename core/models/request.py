from typing import Optional
from pydantic import BaseModel


class RequestBody(BaseModel):
    query: Optional[str] = None
    file: Optional[str] = None