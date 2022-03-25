from pydantic import BaseModel
from typing import List


class GetStatusResponse(BaseModel):
    
    class ResponseDetails(BaseModel):
        links: dict
        steps: List[dict]
        status: str

    Response: ResponseDetails
    AllValidationMessages: List[str]
    ValidationFailureMessages: List[str]
    ValidationWarningMessages: List[str]
    ValidationBusinessRestrictionMessages: List[str]
    IsValid: bool
    CombinedMessages: str

    class Config:
        schema_extra = {
            "example": {
                "Response": {
                    "links": {
                        "Quotation": "link-1",
                        "Proposal": "link-2",
                        "Payslip": "link-3",
                        "Policy": "link-4"
                    },
                    "steps": [{
                        "Quotation": "Done"
                    },
                        {
                        "Proposal": "Done"
                    },
                        {
                        "Payslip": "Done"
                    },
                        {
                        "Policy": "Done"
                    },
                        {
                        "DigitalSignature": "Pending"
                    }
                    ],
                    "status": "Processing"
                },
                "AllValidationMessages": [],
                "ValidationFailureMessages": [],
                "ValidationWarningMessages": [],
                "ValidationBusinessRestrictionMessages": [],
                "IsValid": True,
                "CombinedMessages": ""
            }
        }