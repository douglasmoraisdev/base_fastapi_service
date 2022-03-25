import json
from agristamp_common.utils.logs import logger


def sqs_payload(raw_sqs_payload_body):
    # converte o payload em caso de string
    print(type(raw_sqs_payload_body))
    if type(raw_sqs_payload_body) == str:
        sqs_payload_body = json.loads(raw_sqs_payload_body)
    else:
        sqs_payload_body = raw_sqs_payload_body        

    # valida payload
    if (not 'type' in sqs_payload_body) or (not 'slug' in sqs_payload_body) \
        or (not 'payload' in sqs_payload_body) or (not 'environment' in sqs_payload_body):

        logger.error(f"Payload inválido: {sqs_payload_body}")
        raise Exception(f"Payload inválido: {sqs_payload_body}")

    else:
        event = sqs_payload_body['type']
        slug = sqs_payload_body['slug']
        payload = sqs_payload_body['payload']
        mongo_id = sqs_payload_body['_id']
        environment = sqs_payload_body['environment']

    print(f"Payload recebido: {sqs_payload_body}")

    return event, slug, payload, mongo_id, environment
