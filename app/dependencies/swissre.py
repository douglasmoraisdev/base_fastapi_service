from app.core.utils import swissre_get, swissre_post

from app.models.schemas.simulacao import SimulacaoRequest
from app.models.schemas.proposta import PropostaRequest, PropostaResponse
from app.models.schemas.documento import DocumentoRequest, DocumentoResponse


async def simulacao(
   payload: SimulacaoRequest
):

    general_fields = {
        "productId": payload.product_id,
        "productVersionId": payload.product_version_id,
        "entityTypeId": "SE", # Fixo
        "endorsementTypeId": "1", # Fixo
        "calculationTypeId": payload.cod_reg_agrup.upper(),
        "startDate": payload.start_date,
        "expireDate": payload.expire_date,
        "exemptionTypeId": "3", # Fixo
        "hasFederalSubsidy": payload.has_federal_subsidy,
        "hasStateSubsidy": payload.has_state_subsidy,
        "hasMunicipalSubsidy": False, # Fixo
        "currencyId": "1", # Fixo R$
        "surveyor": None, # Fixo
        "policyholder": None, # enviado apenas quando entityType é Tomador # Fixo
        "insured": {
            "name": payload.insured_name,
            "documentId": payload.insured_document_id
        },
        "beneficiary": {
            "beneficiaryName": payload.insured_name, # mesmo que o insured
            "CPFnumber": payload.insured_document_id # mesmo que o insured
        },
        "brokers": [
        {
            "id": payload.brokers_id,
            "comission": payload.brokers_commission
        }
        ],
        "salesOrganization": {
            "brokerId": "965413261",
            "agencyId": "5320",
            "accountNumber": "123123",
            "postServiceId": "000"
        }
    }

    item_fields = []
    for item in payload.items:

        item_fields.append({
                "discountAndAggrave":"0",
                "dynamicFields": [
                {	
                    "id": "cod_afinidade",
                    "value": item.cod_afinidade
                },
                {	
                    "id": "cod_plano",
                    "value": item.cod_plano
                },
                {	
                    "id": "end_tpenq",
                    "value": item.end_tpenq
                },
                {	
                    "id": "end_classenq",
                    "value": item.end_classenq
                },
                {	
                    "id": "end_tplocal",
                    "value": item.end_tplocal
                },
                {	
                    "id": "cod_reg",
                    "value": payload.cod_reg
                },
                {	
                    "id": "cod_reg_agrup",
                    "value": payload.cod_reg_agrup.upper()
                },
                {	
                    "id": "end_nomris", # Propriedade
                    "value": item.end_nomris
                },
                {	
                    "id": "end_identris", # Valor saca
                    "value": item.end_identris
                },
                {	
                    "id": "end_dataris", # Data Plantio
                    "value": item.end_dataris
                },
                {	
                    "id": "end_arearis", # Area
                    "value": item.end_arearis
                }
                                ],			
                "coverages": [
                    {
                        "id": "00106", # Fixo Cobertura Básica (Granizo,Seca,Geada,Vendaval/Ventos Fortes,Tromba D´água,Chuva Excessiva,Inundação/Alagamento,Variação Excessiva de Temperatura,Raio e Incêndio)
                        "PctFranchise":"0"
                    },                    
                    {
                        "id": "00071", # Fixo Cobertura Replantio (Granizo, Chuva Excessiva e Tromba D´água)
                        "PctFranchise":"0"
                    }
                ],
                "riskArea":
                {
                    "cep": payload.cep,
                    "address": payload.address,
                    "numberOfAddress": payload.numberOfAddress,
                    "complement": payload.complement,
                    "district": payload.district,
                    "unitFederated": payload.unitFederated,
                    "city": payload.city
                },
                "clauseDetails": None
            })

    # Une os campos
    general_fields.update({'items': item_fields})

    swissre_payload = general_fields

    simulacao_request = await swissre_post(swissre_payload, 'issuance/v1/quotation')

    return simulacao_request

async def proposta(
    payload: PropostaRequest,
) -> PropostaResponse:

    swissre_payload = {
        "ContractNumber": payload.contract_number,
        "IssuanceId": 1, # Fixo
        "Insureds": [{
            "Name": payload.insured_name,
            "DocumentId": payload.insured_document,
            "PersonTypeId": payload.insured_persontype,
            "Email": payload.insured_email,
            "ActivityId": payload.insured_activityid if payload.insured_activityid else "20932", # TODO retirar esse default se for obrigatorio
            "Addresses": [{
                    "TypeId": "RE",
                    "ZipCode": payload.insured_address_zipcode,
                    "Street": payload.insured_address_street,
                    "Number": payload.insured_address_number,
                    "CityId": payload.insured_address_cityid,
                    "StateId": payload.insured_address_stateid.upper(), #uf
                    "CountryId": 1058, # Fixo - Brasil
                    "Email": payload.insured_email,
                    "Neighborhood": payload.insured_address_neighborhood,
                    "Telephones": [{
                        "TypeId": payload.insured_phone_typeid,
                        "AreaCode": payload.insured_phone_areacode,
                        "Number": payload.insured_phone_number
                    }]
            }],
        }],
        "ChargeTypeId": payload.chargetypeid,
        "InstallmentNumber": payload.installmentnumber,
        "WordingPolicyObject": {
            "Id": "01"
        },
        "WordingPrivateAttachment": {
            "Id": "01"
        },
        "WordingSpecialAttachment": {
            "Id": "02"
        }
    }

    # Coordenadas:
    geographical_coordinates = {"geographicalCoordinates": []}
    for coordinate in payload.coordinates:

        coordinates = []
        for item in coordinate:

            coordinates.append({
                            "itemCode": item.item,
                            "latitude": item.latitude,
                            "longitude": item.longitude
                        })

        geographical_coordinates["geographicalCoordinates"].append({"coordinates": coordinates})

    swissre_payload.update(geographical_coordinates)

    proposta_request = await swissre_post(swissre_payload, 'issuance/v1/proposal')

    result = proposta_request

    return result


async def get_status(id_proposta: str,
                     proposalNumber: str = None
):

    params = {"contractNumber": id_proposta,
              "issuanceId": "1"}

    if proposalNumber:
        params["proposalNumber"] = proposalNumber

    request = await swissre_get('issuance/v1/status', params)

    return request


async def get_documento(
    payload: DocumentoRequest,
) -> DocumentoResponse:

    swissre_payload = {
        "TypeId": payload.document_type,
        "ContractNumber": payload.contract_number,
        "IssuanceId": "1",
    }

    documento = await swissre_post(swissre_payload, 'document/v1/', download_pdf=True)

    result = {
        "document_type": payload.document_type,
        "document": documento
    }

    return result
