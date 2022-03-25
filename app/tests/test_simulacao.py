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

def test_health_check():
    response = client.get("/swissre_service/health")
    assert response.status_code == 200


def test_get_simulacao():

    payload = {
        "product_id": "01377",
        "product_version_id": "2021_2022_11",
        "cod_reg": "20248",
        "cod_reg_agrup": "SP",
        "start_date": "2021-09-26T00:00:00-03:00",
        "expire_date": "2022-09-26T00:00:00-03:00",
        "has_federal_subsidy": True,
        "has_state_subsidy": False,
        "insured_name": "Joao da Silva",
        "insured_document_id": "10220925000100",
        "brokers_id": "0203257",
        "brokers_commission": "10",
        "items": [
            {
            "cod_afinidade": "75768",
            "cod_plano": "00001",
            "end_tpenq": "13",
            "end_classenq": "40004",
            "end_tplocal": "0265",
            "end_nomris": "Talhao 2",
            "end_identris": 130,
            "end_dataris": "11/11/2021",
            "end_arearis": 50
            }
        ],
        "cep": "86015010",
        "address": "Av Higienopolis",
        "numberOfAddress": "12",
        "complement": "",
        "district": "ZONA RURAL",
        "unitFederated": "SP",
        "city": "Assis"
    }

    response = client.post("/swissre_service/simulacao", headers=headers, data=json.dumps(payload))

    assert response.status_code == 200
