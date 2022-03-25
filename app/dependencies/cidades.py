from app.core.utils import (swissre_auth, swissre_error_messages, swissre_post)
from app.models.schemas.cidades import CidadesResponse
from starlette.exceptions import HTTPException


async def cidades_by_uf(
    product_id: str,
    product_version_id: str,
    uf: str
):

    swissre_payload = {
        "items" : [
            {
                    "KeyName":"cod_localizacao",
                    "ProductId": product_id,
                    "ProductVersionId":product_version_id,
                    "RegionCode": uf.upper()
            }
        ]
    }


    auth_token = await swissre_auth()

    cidades_request = await swissre_post(swissre_payload, 'productconfiguration/v1/GetDomainTypes', auth_token=auth_token)

    if cidades_request.status_code == 200:

        if 'values' in cidades_request.json()[0]:
            return CidadesResponse(**{'response': cidades_request.json()[0]['values']})
        else:
            raise HTTPException(500, cidades_request.text)
    else:
        raise swissre_error_messages(cidades_request)
