from fastapi import APIRouter, Depends

from app.dependencies.afinidade import afinidade
from app.dependencies.cidades import cidades_by_uf

from app.models.schemas.afinidade import AfinidadeResponse
from app.models.schemas.cidades import CidadesResponse


router = APIRouter()


@router.post(
    "/afinidade",
    response_model=AfinidadeResponse,
    name="Swiss Re:  Retorna o codigo da Afinidade",
    tags=['api v1 - dominios']
)
async def _afinidade(
    afinidade: AfinidadeResponse = Depends(afinidade),
) -> AfinidadeResponse:

    return afinidade


@router.get(
    "/cidades_by_uf",
    response_model=CidadesResponse,
    name="Swiss Re:  Retorna os ids das cidades por UF",
    tags=['api v1 - dominios']
)
async def _cidades(
    cidades: CidadesResponse = Depends(cidades_by_uf),
) -> CidadesResponse:

    return cidades
