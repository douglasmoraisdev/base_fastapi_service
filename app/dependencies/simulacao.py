from fastapi import HTTPException, Header
from app.core.utils import (swissre_auth, swissre_error_messages, swissre_get,
                            swissre_post, save_payload)
from app.models.schemas.simulacao import SimulacaoRequest, SimulacaoResponse



async def get_installments(
    contract_number: str,
    billing_type_first_installment: str,
    billing_type_other_installments: str,
    auth_token: str = None
):
    params = {
        "contractNumber": contract_number,
        "billingTypeFirstInstallment": billing_type_first_installment,
        "billingTypeOtherInstallments": billing_type_other_installments,
        "IssuanceId": 1  # Fixo
    }
    response = await swissre_get('productconfiguration/v1/PaymentTypes', params, auth_token=auth_token)

    return response['Response']


async def get_risk_infos(
    payload_simulacao: SimulacaoRequest,
    auth_token: str = None
):
    item = payload_simulacao.items[0]

    payload = {
        "BrokerId": "965413261",
        "FramingId": item.end_tpenq,
        "LocationId": payload_simulacao.cod_reg,
        "RegionId": payload_simulacao.cod_reg_agrup,
        "CategoryId": item.end_tplocal,
        "ProductId": payload_simulacao.product_id,
        "VersionDate": payload_simulacao.product_version_date
    }

    response = await swissre_post(payload, 'productconfiguration/v1/GetPreDefinedValues', auth_token=auth_token)

    if response.status_code == 200:

        if response.json()['IsValid']:
            return response.json()['Response'][0]
        else:
            raise HTTPException(500, response.text)
    else:
        raise swissre_error_messages(response)


async def simulacao(
    payload: SimulacaoRequest,
    Hash: str = Header(default=None),
):

    async def _response_simulacao(
            simulacao: dict,
            payload_request_simulacao: SimulacaoRequest,
            auth_token: str = None) -> SimulacaoResponse:

        contract_number = simulacao['Response'].get('contractNumber')

        installments = await get_installments(contract_number,
                                              payload_request_simulacao.billing_type_first_installment,
                                              payload_request_simulacao.billing_type_other_installments,
                                              auth_token=auth_token)
        simulacao['Response']['installments'] = installments

        risk_infos = await get_risk_infos(payload_request_simulacao, auth_token=auth_token)

        simulacao['Response']['initialReferentialRisk'] = risk_infos.get(
            'initialReferentialRisk', 0)
        simulacao['Response']['referentialRiskLimit'] = risk_infos.get(
            'referentialRiskLimit', 0)

        return SimulacaoResponse(**simulacao)


    async def _save_simulacao(simulacao_request, payload, swissre_payload):

        # salva o request
        await save_payload(Hash, 'simulacao', payload, original_payload=swissre_payload)

        # salva o retorno
        extras = {'cod_cotacao': ''}
        if hasattr(simulacao_request, 'json'):
            original_return = simulacao_request.json()

            # atualiza cod_cotacao se existir
            if 'Response' in original_return:
                if 'contractNumber' in original_return['Response']:
                    extras = {'cod_cotacao': original_return['Response']['contractNumber']}

        else:
            original_return = simulacao_request.text

        await save_payload(Hash, 'simulacao', payload, original_return=original_return, extras=extras)


    general_fields = {
        "productId": payload.product_id,
        "productVersionId": payload.product_version_id, # payload.product_version_id,
        "entityTypeId": "SE",  # Fixo
        "endorsementTypeId": "1",  # Fixo
        "calculationTypeId": "SP", # Fixo
        "startDate": payload.start_date,
        "expireDate": payload.expire_date,
        "exemptionTypeId": "3",  # Fixo
        "hasFederalSubsidy": payload.has_federal_subsidy,
        "hasStateSubsidy": payload.has_state_subsidy,
        "hasMunicipalSubsidy": False,  # Fixo
        "currencyId": "1",  # Fixo R$
        "surveyor": None,  # Fixo
        "policyholder": None,  # enviado apenas quando entityType é Tomador # Fixo
        "insured": {
            "name": payload.insured_name,
            "documentId": payload.insured_document_id
        },
        "beneficiary": {
            "beneficiaryName": payload.insured_name,  # mesmo que o insured
            "CPFnumber": payload.insured_document_id  # mesmo que o insured
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
    item_no = 1
    for item in payload.items:

        async def _get_questions():

            default_questions = [] # get from mongo

            other_questions = [
                {
                "id": "30", # "Data Final do Plantio:"
                "value": "2022-06-21T00:00:00-03:00", # mock
                },
                {
                "id": "45", # "Optou pela Subvenção Estadual no Paraná?"
                "value": "2", # ou 1-sim
                },
                {
                "id": "46", # "Optou pela Subvenção Estadual no Paraná?"
                "value": "", # texto livre
                },

            ]

            questions = default_questions + other_questions

            return questions

        questions = await _get_questions()

        item_fields.append({
            "discountAndAggrave": "0",
            "dynamicFields": [
                {
                    "id": "cod_item",
                    "value": item_no
                },
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
                    "id": "end_nomris",  # Propriedade
                    "value": item.end_nomris
                },
                {
                    "id": "end_identris",  # Valor saca
                    "value": item.end_identris
                },
                {
                    "id": "end_dataris",  # Data Plantio
                    "value": item.end_dataris
                },
                {
                    "id": "end_arearis",  # Area
                    "value": item.end_arearis
                }
            ],
            "questions": questions,
            "coverages": [
                {
                    # Fixo Cobertura Básica (Granizo,Seca,Geada,Vendaval/Ventos Fortes,Tromba D´água,Chuva Excessiva,Inundação/Alagamento,Variação Excessiva de Temperatura,Raio e Incêndio)
                    "id": "00106",
                    "PctFranchise": "0"
                },
                {
                    # Fixo Cobertura Replantio (Granizo, Chuva Excessiva e Tromba D´água)
                    "id": "00071",
                    "PctFranchise": "0"
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

        item_no += 1

    # Une os campos
    general_fields.update({'items': item_fields})

    swissre_payload = general_fields

    auth_token = await swissre_auth()

    simulacao_request = await swissre_post(swissre_payload, 'issuance/v1/quotation', auth_token=auth_token)

    await _save_simulacao(simulacao_request, payload.dict(), swissre_payload)

    if simulacao_request.status_code == 200:

        if simulacao_request.json()['IsValid']:
            return await _response_simulacao(simulacao_request.json(), payload, auth_token=auth_token)
        else:
            raise HTTPException(500, simulacao_request.text)
    else:
        raise swissre_error_messages(simulacao_request)
