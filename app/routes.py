from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.dependencies.swissre import get_documento

from app.dependencies.simulacao import simulacao
from app.dependencies.proposta import proposta
from app.dependencies.status import status

from app.models.schemas.simulacao import SimulacaoResponse
from app.models.schemas.proposta import PropostaResponse
from app.models.schemas.status import GetStatusResponse
from app.models.schemas.documento import DocumentoResponse, DocumentoRequest


router = APIRouter()


@router.post(
    "/simulacao",
    response_model=SimulacaoResponse,
    name="Swiss Re:  Cria nova cotacao",
    tags=['api v1']
)
async def _simulacao(
    proposta: SimulacaoResponse = Depends(simulacao),
) -> SimulacaoResponse:

    return proposta


@router.post(
    "/proposta",
    status_code=HTTP_201_CREATED,
    response_model=PropostaResponse,
    name="Swiss Re:  Cria nova proposta",
    tags=['api v1']
)
async def _proposta(
    proposta: PropostaResponse = Depends(proposta),
) -> PropostaResponse:

    return proposta


@router.get(
    "/status_proposta/{id_proposta}",
    response_model=GetStatusResponse,
    name="Swiss Re: Obter os detalhes das etapas da emissão solicitada.",
    tags=['api v1']
)
async def _status_proposta(
    status: GetStatusResponse = Depends(status)
) -> GetStatusResponse:

    return status


@router.post(
    "/consulta_documento",
    response_model=DocumentoResponse,
    name="Swiss Re:  Consulta de documento",
    tags=['api v1']
)
async def _get_documento(
    documento: DocumentoRequest = Depends(get_documento),
) -> DocumentoResponse:

    return documento
