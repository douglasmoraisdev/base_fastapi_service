from pydantic import BaseModel
from typing import List


class CidadesResponse(BaseModel):

    class CidadesList(BaseModel):
        id: str
        description: str

    response: List[CidadesList]
