from app.core.utils import swissre_get
from app.core.utils import send_status_sqs

async def status(
    payload: str,
    mongo_id: str,
    environment: str
):

    cd_proposta = payload['id_proposta']
    hash_proposta_legado = payload['hash_proposta_legado']

    url = f'issuance/v1/status?contractNumber={cd_proposta}&issuanceId=1'

    #if proposalNumber:
    #    url = f'{url}&proposalNumber={proposalNumber}'

    request = await swissre_get(url, {})

    update_status_proposta('atualizando-status', request, mongo_id, environment)

    return request


def update_status_proposta(new_status, status_detail={}, proposta_id='', environment=''):

    return send_status_sqs(new_status, status_detail, proposta_id, environment)
