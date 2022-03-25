from pydantic import BaseModel
from typing import List


class AfinidadeRequest(BaseModel):

    product_id: str
    product_version_id: str
    broker_id: str
    insured_id: str
    beneficiary_id: str
    cod_ocup: str
    cod_enqdr: str
    end_tplocal: str
    cod_reg_agrup: str
    cod_reg: str


class AfinidadeResponse(BaseModel):

    class AfinidadeList(BaseModel):
        id: str
        description: str

    response: List[AfinidadeList]

'''
{
    "ProductId":"01052",
    "ProductVersionId":"2022_1",
    "BrokerId":"965413261",
    "InsuredId":"80140447",
    "BeneficiaryId":"90074643",

    "DynamicFields": [
    {
        "Value": "14",
        "metadataColumnName": "cod_ocup",
        "targetTable": "ems_item_local_risco",
        "targetColumnName": "end_tpenq",
        "sequenceNumber": 3
    },
    {
        "Value": "00001",
        "metadataColumnName": "cod_enqdr",
        "targetTable": "ems_item_local_risco",
        "targetColumnName": "end_classenq",
        "sequenceNumber": 4
    },
    {
        "Value": "0365",
        "metadataColumnName": "cod_categ",
        "targetTable": "ems_item_local_risco",
        "targetColumnName": "end_tplocal",
        "sequenceNumber": 5
    },
    {
        "Value": "PR",
        "metadataColumnName": "cod_reg",
        "targetTable": "ems_item_local_risco",
        "targetColumnName": "cod_reg_agrup",
        "sequenceNumber": 6
    },
    {
        "Value": "30836",
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
'''