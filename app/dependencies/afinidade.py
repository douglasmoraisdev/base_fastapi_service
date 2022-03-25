from app.core.utils import (swissre_auth, swissre_error_messages, swissre_post)
from app.models.schemas.afinidade import AfinidadeRequest, AfinidadeResponse
from starlette.exceptions import HTTPException


async def afinidade(
    payload: AfinidadeRequest
):

    swissre_payload = {
        "ProductId": payload.product_id,
        "ProductVersionId": payload.product_version_id,
        "BrokerId":"965413261", # payload.broker_id
        "InsuredId":"80140447", # payload.insured_id
        "BeneficiaryId":"90074643", # payload.beneficiary_id

        "DynamicFields": [
        {
            "Value": payload.cod_ocup,
            "metadataColumnName": "cod_ocup",
            "targetTable": "ems_item_local_risco",
            "targetColumnName": "end_tpenq",
            "sequenceNumber": 3
        },
        {
            "Value": payload.cod_enqdr,
            "metadataColumnName": "cod_enqdr",
            "targetTable": "ems_item_local_risco",
            "targetColumnName": "end_classenq",
            "sequenceNumber": 4
        },
        {
            "Value": payload.end_tplocal,
            "metadataColumnName": "cod_categ",
            "targetTable": "ems_item_local_risco",
            "targetColumnName": "end_tplocal",
            "sequenceNumber": 5
        },
        {
            "Value": payload.cod_reg_agrup,
            "metadataColumnName": "cod_reg",
            "targetTable": "ems_item_local_risco",
            "targetColumnName": "cod_reg_agrup",
            "sequenceNumber": 6
        },
        {
            "Value":  payload.cod_reg,
            "metadataColumnName": "cod_localizacao",
            "targetTable": "ems_item_local_risco",
            "targetColumnName": "cod_reg",
            "sequenceNumber": 7
        },
        {
            "metadataColumnName": "cod_afinidade",
            "targetTable": "ems_item_local_risco",
            "targetColumnName": "cod_afinidade",
            "sequenceNumber": 194
        }
        ]
    }

    auth_token = await swissre_auth()

    afinidade_request = await swissre_post(swissre_payload, f'productconfiguration/v1/GetAffinityRate?productId={payload.product_id}', auth_token=auth_token)

    if afinidade_request.status_code == 200:

        if 'id' in afinidade_request.json()[0]:
            return AfinidadeResponse(**{'response': afinidade_request.json()})
        else:
            raise HTTPException(500, afinidade_request.text)
    else:
        raise swissre_error_messages(afinidade_request)
