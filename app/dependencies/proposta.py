from app.core.utils import save_payload
from app.core.utils import swissre_post, swissre_error_messages
from app.dependencies.status import update_status_proposta
from app.models.schemas.proposta import PropostaRequest, PropostaResponse

async def proposta(
    payload: PropostaRequest,
    proposta_id: str,
    environment: str
) -> PropostaResponse:

    def _get_address_id():

        if payload.insured_persontype == "F":
            address_type = "RE"
        else:
            address_type = "CM"

        return address_type


    def _get_beneficiaries():

        beneficiaries_list = []
        for beneficiary in payload.beneficiaries:

            # PF
            if len(beneficiary.cpfnumber) == 11:
                personType = "F"
                addresses_typeId = "RE"

            # PJ
            else:
                personType = "J"
                addresses_typeId = "CM"

            beneficiaries_list.append(
                {
                    "personType": personType,
                    "CPFNumber": beneficiary.cpfnumber,
                    "BeneficiaryName": beneficiary.beneficiaryname,
                    "expectationID": beneficiary.expectationid,
                    "isPercentage": beneficiary.ispercentage,
                    "issuanceId": beneficiary.issuanceid,
                    "itemCode": beneficiary.itemcode,
                    "itemCodeUpdated": False,
                    "percentage": beneficiary.percentage,
                    "addresses": [
                        {
                            "typeId": addresses_typeId,
                            "zipCode": beneficiary.address_zipcode,
                            "countryId": 1058, # Brasil
                            "street": beneficiary.address_street,
                            "number": beneficiary.address_number,
                            "cityId": beneficiary.address_cityid,
                            "stateId": beneficiary.address_stateid , #UF
                            "email": beneficiary.address_email,
                            "neighborhood": beneficiary.address_neighborhood,
                            "Telephones": [
                                {
                                    "TypeId": beneficiary.telephone_typeid,
                                    "AreaCode": beneficiary.telephone_areacode,
                                    "Number": beneficiary.telephone_number
                                }
                            ]
                        }
                    ]
                }
            )


        return beneficiaries_list


    async def _save_proposta(proposta_request, payload, swissre_payload):

        # salva o request
        await save_payload(proposta_id, 'proposta', payload, original_payload=swissre_payload)

        # salva o retorno
        extras = {'cod_cotacao': payload['contract_number']}
        if hasattr(proposta_request, 'json'):
            original_return = proposta_request.json()
        else:
            original_return = proposta_request.text

        await save_payload(proposta_id, 'proposta', payload, original_return=original_return, extras=extras)



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
                    "TypeId": _get_address_id(),
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
        "beneficiaryDetails": _get_beneficiaries(),
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

    try:
        proposta_request = await swissre_post(swissre_payload, 'issuance/v1/proposal')

        await _save_proposta(proposta_request, payload.dict(), swissre_payload)

    except Exception as e:
        print(f'Atualizado status da proposta para [erro-envio] {str(e)}')
        update_status_proposta('erro-envio', {'errors': str(e)}, proposta_id, environment)
        return False

    if proposta_request.status_code == 200:

        if proposta_request.json()['IsValid']:

            cod_cotacao = payload.contract_number
            detail_sucesso = {'cod_cotacao': cod_cotacao}

            print('Atualizado status da proposta para [enviado-seguradora]')
            update_status_proposta('enviado-seguradora', detail_sucesso, proposta_id, environment)
            return True

        else:
            print('Atualizado status da proposta para [erro-envio]')
            update_status_proposta('erro-envio', {'errors': proposta_request.text}, proposta_id, environment)
            return False
    else:

        try:
            error_message =  swissre_error_messages(proposta_request)

        except Exception as e:
            error_message = e.detail

        finally:

            print('Atualizado status da proposta para [erro-envio]')
            update_status_proposta('erro-envio', {'errors': [str(error_message)]}, proposta_id, environment)
            return False
