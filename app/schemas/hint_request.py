from pydantic import BaseModel


class HintRequest(BaseModel):
    code: str
    output: str
    error: str
    status: str
