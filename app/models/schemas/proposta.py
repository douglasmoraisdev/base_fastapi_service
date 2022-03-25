from pydantic import BaseModel
from typing import List


class PropostaRequest(BaseModel):


    class Beneficiaries(BaseModel):

        cpfnumber: str
        beneficiaryname: str
        expectationid: int = 0
        ispercentage: bool
        issuanceid: str
        itemcode: str
        itemcodeupdated: bool = False
        percentage: str

        address_zipcode: str
        address_countryid: str = '1058'
        address_street: str
        address_number: str
        address_cityid: str
        address_stateid: str
        address_email: str
        address_neighborhood: str

        telephone_typeid: str
        telephone_areacode: str
        telephone_number: str


    class Coordinates(BaseModel):
        item: int
        latitude: str
        longitude: str

    contract_number: str
    insured_name: str
    insured_document: str
    insured_persontype: str # F ou J
    insured_email: str
    insured_activityid: str # Profissao TODO

    insured_address_zipcode: str
    insured_address_street: str
    insured_address_number: str
    insured_address_cityid: str # Cidade por extenso
    insured_address_stateid: str
    insured_address_neighborhood: str

    insured_phone_typeid: str
    insured_phone_areacode: str
    insured_phone_number: str

    beneficiaries: List[Beneficiaries]

    chargetypeid: str # 0403
    installmentnumber: int # numero de parcelas

    coordinates: List[List[Coordinates]]


class PropostaResponse(BaseModel):

    Status: int
    AllValidationMessages: List[str]
    ValidationFailureMessages: List[str]
    ValidationWarningMessages: List[str]
    ValidationBusinessRestrictionMessages: List[str]
    IsValid: bool
    CombinedMessages: str
