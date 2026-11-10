from pydantic import BaseModel
from typing import Any

class BaseResponse(BaseModel):
    message : str
    data : Any = None


class ContData(BaseModel):
    description: str | None = None
    amount: float

class ContResponse(BaseResponse):
    data : dict[int, ContData] | ContData

