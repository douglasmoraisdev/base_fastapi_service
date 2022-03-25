from pydantic import BaseModel


class DocumentoRequest(BaseModel):

    contract_number: str
    document_type: str


class DocumentoResponse(BaseModel):

    document_type: str
    document: str
