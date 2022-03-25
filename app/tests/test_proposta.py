import os
import json
from dotenv import load_dotenv

load_dotenv()

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

headers = {
    'Authorization': 'Bearer '+os.getenv('AGRISTAMP_KEY')
}


def test_post_proposta():

    payload = {
        "contract_number" : "020101523189",
        "insured_name" : "JOAO DA SILVA",
        "insured_document" : "61154373000101",
        "insured_persontype" : "J",
        "insured_email" : "teste@gmail.com",
        "insured_activityid" : "20932",
        "insured_address_zipcode" : "01451001",
        "insured_address_street" : "AVENIDA FARIA LIMA",
        "insured_address_number" : "3333",
        "insured_address_cityid" : "Sao Paulo",
        "insured_address_stateid" : "SP",
        "insured_address_neighborhood" : "ZONA RURAL",
        "insured_phone_typeid" : "FI",
        "insured_phone_areacode" : "11",
        "insured_phone_number" : "30730000",
        "chargetypeid" : "0403",
        "installmentnumber" : 1,
        "coordinates": [
                    [
                        {
                            "item": 1,
                            "latitude": -10,
                            "longitude": 51,
                        },
                        {
                            "item": 1,
                            "latitude": -11,
                            "longitude": 52,
                        },
                        {
                            "item": 1,
                            "latitude": -12,
                            "longitude": 53,
                        },
                        {
                            "item": 1,
                            "latitude": -13,
                            "longitude": 54,
                        }
                    ]
                ]
        }
        
    response = client.post("/swissre_service/proposta", headers=headers, data=json.dumps(payload))

    assert response.status_code in [200, 201]
