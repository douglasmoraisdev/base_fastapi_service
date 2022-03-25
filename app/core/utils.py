import debugpy
import boto3
import requests
import json
import pika
from datetime import datetime
from fastapi import HTTPException

from app.core.config import (QUEUE_URL_PROPOSTAS_PUB_SERVICE,
                            DEV,
                            AWS_DEFAULT_REGION,
                            AWS_ACCESS_KEY_ID,
                            AWS_SECRET_ACCESS_KEY,
                            SERVICE_SLUG,
                            VERIFY_SSL,
)
from app.db.mongo import payload_collection
from app.core import config
from agristamp_common.utils.logs import logger


def set_trace():
    debugpy.listen(("0.0.0.0", 5678))


async def swissre_auth():

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': config.SWISSRE_AUTH_TOKEN
    }

    username = config.SWISSRE_USERNAME
    password = config.SWISSRE_PASSWORD
    client_id = config.SWISSRE_CLIENT_ID
    body = f'username={username}&password={password}&grant_type=password&client_id={client_id}'

    print(body)

    request = requests.post(config.SWISSRE_API_AUTH_URL, data=body, headers=headers, verify=VERIFY_SSL)

    if request.status_code == 200:
        return request.json()['access_token']
    else:
        raise HTTPException(request.status_code, request.text)


async def swissre_get(endpoint, params: dict = {}, auth_token=None):

    if not auth_token:
        auth_token = await swissre_auth()

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config.SWISSRE_AUTH_TOKEN,
        'Authorization': f'Bearer {auth_token}'
    }

    endpoint_url = f"{config.SWISSRE_API_URL}{endpoint}"

    status_request = requests.get(url=endpoint_url, params=params, headers=headers, verify=VERIFY_SSL)

    # Log
    print('Disparado GET para parceiro - SwissRe')

    print('REQUEST ----------------')
    print(endpoint_url)
    print(json.dumps(params))

    print('RESPONSE ----------------')
    print(f'status_request.status_code {status_request.status_code}')
    print(f'status_request.json() {status_request.json()}')

    if status_request.status_code == 200:
        if status_request.json()['IsValid']:
            return status_request.json()
        else:
            raise HTTPException(500, status_request.text)
    else:
        raise HTTPException(status_request.status_code, status_request.text)


async def swissre_post(payload, endpoint, download_pdf: bool = False, auth_token=None):

    if not auth_token:
        auth_token = await swissre_auth()

    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': config.SWISSRE_AUTH_TOKEN,
        'Authorization': f'Bearer {auth_token}'
    }

    endpoint_url = f"{config.SWISSRE_API_URL}{endpoint}"

    swissre_request = requests.post(url=endpoint_url, data=json.dumps(payload), headers=headers, verify=VERIFY_SSL)

    # Log
    print('Disparado POST para parceiro - SwissRe')

    print('REQUEST ----------------')
    print(endpoint_url)
    print(json.dumps(payload))

    print('RESPONSE ----------------')
    print(f'swissre_request.status_code {swissre_request.status_code}')
    print(f'swissre_request.text {swissre_request.text}')

    return swissre_request

    '''
    if swissre_request.status_code == 200:
        if download_pdf:
           return swissre_request.text

        if swissre_request.json()['IsValid']:
            return swissre_request.json()
        else:
            raise HTTPException(500, swissre_request.text)
    else:
        raise swissre_error_messages(swissre_request)
    '''


def swissre_error_messages(swissre_request):

    if 'json' in dir(swissre_request) and (swissre_request.text != ''):
        error_response = swissre_request.json()

        if not error_response['IsValid']:
            raise HTTPException(500, error_response['CombinedMessages'].strip())
        else:
            raise HTTPException(500, error_response.strip())

    else:
        error_response = swissre_request.text.strip()
        raise HTTPException(swissre_request.status_code, error_response)


def sqs_send(payload):

    queue_url = QUEUE_URL_PROPOSTAS_PUB_SERVICE

    def sqs_send_prod(payload):

        client = boto3.client(service_name='sqs',
                            region_name=AWS_DEFAULT_REGION,
                            aws_access_key_id=AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                            endpoint_url=queue_url)

        result = client.send_message(QueueUrl=queue_url,
                                    MessageBody=json.dumps(payload))

        return result


    def sqs_send_dev(payload):

        def send_rabbitmq(payload):

            import pika

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.1'))
            channel = connection.channel()

            channel.queue_declare(queue=queue_url)

            channel.basic_publish(exchange='', routing_key=queue_url, body=json.dumps(payload))
            print(f" [x] Sent: {payload}")
            connection.close()

        lambda_trigger_payload = {
            "Records": [
            {
                "MessageId": "dev-19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": payload,
                "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1523232000000",
                "SenderId": "123456789012",
                "ApproximateFirstReceiveTimestamp": "1523232000001"
                },
                "messageAttributes": {},
                "md5OfBody": "{{{md5_of_body}}}",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                "awsRegion": "us-east-1"
            }
            ]
        }

        # Chama o propostas_sub async
        send_rabbitmq(lambda_trigger_payload)
        return {'MessageId': 'Send via RabbitMQ'}

    # Trata envio de fila em dev(rabbitMQ) e prod(AWS Sqs)
    if (DEV == '1') or (DEV == 1):
        print('Enviando status via RabbitMQ (DEV)')
        return sqs_send_dev(payload)
    else:
        print(f'Enviando status via SQS - [{queue_url}]')
        return sqs_send_prod(payload)


def send_status_sqs(new_status, status_detail, mongo_id, environment, type='status'):
    sqs_payload = {
        "slug": 'swissre-seguradora',
        "_id": mongo_id,
        "type": type,
        "payload": status_detail,
        "new_status": new_status,
        "environment": environment
    }

    sqs_result = sqs_send(sqs_payload)

    return sqs_result['MessageId']


async def save_payload(hash_proposta: str, endpoint:str, json_payload: dict={}, original_payload: str='', original_return: str='', extras={}):

    try:
        query = {"hash_proposta": hash_proposta, "endpoint": endpoint}

        values = {}
        if json_payload:
            values.update({"json_payload": json.dumps(json_payload)})

        if original_payload:
            values.update({"original_payload": original_payload})

        if original_return:
            values.update({"original_return": original_return})


        if extras:
            values.update({"cod_cotacao": extras['cod_cotacao']})


        values.update({"updated_at": datetime.strftime(datetime.now(), '%d/%m/%Y %H:%M:%S')})

        update_set = {"$set": values}

        await payload_collection.update_one(query, update_set, upsert=True)

    except Exception as e:
        logger.error(f'Erro ao salvar payload {str(e)}')
