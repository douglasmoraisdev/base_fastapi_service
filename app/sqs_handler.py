from __future__ import print_function

from app.dependencies.proposta import proposta
from app.dependencies.status import status

from app.models.schemas.proposta import PropostaRequest

from app.sqs_parser import sqs_payload

async def sqs_handler(event, context):

    for record in event['Records']:
        raw_sqs_payload_body = record["body"]

        # payload do sqs
        event, slug, payload, mongo_id, environment = sqs_payload(raw_sqs_payload_body)

        try:
            if event == "proposta":
                return await proposta(PropostaRequest(**payload), mongo_id, environment)

            elif event == "status":
                return await status(payload, mongo_id, environment)

            else:
                raise Exception(f"Evento invalido: {event}")

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(f'Erro ao executar {str(e)}')
