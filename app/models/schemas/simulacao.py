from pydantic import BaseModel
from typing import List


class SimulacaoRequest(BaseModel):

    class ItemSimulacao(BaseModel):

        # Campos dinamicos
        cod_afinidade: str
        cod_plano: str
        end_tpenq: str
        end_classenq: str
        end_tplocal: str
        end_nomris: str
        end_identris: float
        end_dataris: str
        end_arearis: str

    product_id: str
    product_version_id: str
    product_version_date: str
    cod_reg: str
    cod_reg_agrup: str
    start_date: str  # "2021-09-26T00:00:00-03:00"
    expire_date: str  # "2022-09-26T00:00:00-03:00"
    has_federal_subsidy: bool = False
    has_state_subsidy: bool = False
    insured_name: str
    insured_document_id: str
    brokers_id: str
    brokers_commission: str
    #salesorganization_brokerid: str
    #salesorganization_agencyid: str
    #salesorganization_accountnumber: str
    #salesorganization_postserviceid: str
    items: List[ItemSimulacao]
    # riskArea
    cep: str
    address: str
    numberOfAddress: str
    complement: str
    district: str
    unitFederated: str
    city: str
    billing_type_first_installment: str
    billing_type_other_installments: str


class SimulacaoResponse(BaseModel):


    class ResponseSimulacao(BaseModel):


        class InstallmentsSimulacao(BaseModel):

            installmentNumber: int
            paymentCode: str
            paymentDescription: str
            individualInstallmentAmount: float
            remainingInstallmentAmount: float
            federalSubsidy: float
            stateSubsidy: float
            totalAmount: float
            paymentTypeFirstInstallment: str
            paymentTypeOthersInstallments: str


        contractNumber: str
        issuanceId: int
        proposalNumber: int = None
        premiumAmount: float
        insuredAmount: float
        installments: List[InstallmentsSimulacao]
        initialReferentialRisk: float
        referentialRiskLimit: float

    Response: ResponseSimulacao
    AllValidationMessages: List[str]
    ValidationFailureMessages: List[str]
    ValidationWarningMessages: List[str]
    ValidationBusinessRestrictionMessages: List[str]
    IsValid: bool
    CombinedMessages: str
