#!/bin/bash

# stack com image
echo "-- cloudformation create-stack ecr"
awslocal cloudformation create-stack \
--stack-name stack-ecr-swissre-service \
--template-body file://localstack/image.stack.json \
--parameters ParameterKey=ECRrepositoryName,ParameterValue=swissre_service

# envia imagem para o container
echo "-- docker build"
docker build -t localhost:4510/swissre_service .

echo "-- docker tag"
docker tag swissre_service:latest localhost:4510/swissre_service:latest

echo "-- docker push"
docker push localhost:4510/swissre_service

# cria a stack do serviço
echo "-- cloudformation create-stack endpoint"
awslocal cloudformation create-stack --stack-name stack-endpoint-swissre-service --template-body file://localstack/endpoint.stack.json


# carrega as configurações do arquivo
filename='localstack/lambda_variables.ini'
config_str=''
while read line; do
# reading each line
config_str=$config_str$line
done < $filename

# atualiza as variaveis da lambda
echo "-- lambda update-function-configuration"
awslocal lambda update-function-configuration --function-name swissre_service_function --environment 'Variables={'$config_str'}'
