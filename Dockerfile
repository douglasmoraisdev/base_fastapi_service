FROM fastapi_base:latest

# service args to variables

# default
ENV DEBUG='0'

COPY ./app ${LAMBDA_TASK_ROOT}/app

RUN pip install -r ${LAMBDA_TASK_ROOT}/app/requirements.txt

CMD [ "app.handler.lambda_handler" ]
