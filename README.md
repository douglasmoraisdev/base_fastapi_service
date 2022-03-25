# Swiss Re Service

Microserviço para conexão e integração com a API do parceiro Swiss Re.

## Sobre a PEP-8

A PEP-8 é o conjunto oficial de convenções de código adotados pela comunidade Python.

Este projeto implementa as diretrizes de design de código do [PEP-8](https://www.python.org/dev/peps/)



## Framework FastAPI
O projeto roda sobre o framework FastAPI. Para mais informações e documentação [clique aqui](https://fastapi.tiangolo.com/)



## Estrutura de diretórios

    app                             - diretorio do aplicativo
    ├── core                        - classes e funções globais
    │   ├── config.py               - contém o mapeamento das variáveis de ambiente de configuração
    │   └── utils.py                - funções auxiliares globais, ex.: debug, logs, conversor de data, etc.
    ├── db                          - classes relacionadas a conexão de banco de dados
    │   ├── migrations              - migrações de db, utilizado pelo Alembic
    │   └── base.py                 - classe base dos models, utilizado pelo SQLAlchemy
    ├── dependencies                - lógica de negócio principal
    │   └── xyz_crud.py             - lógica de CRUD
    ├── errors                      - classes de tratamento de erros
    │   ├── http_error.py           - handler dos erros de HTTP
    │   └── validation_erros.py     - handler dos erros de validação de dados
    ├── models                      - modelos de dados
    │   ├── domain                  - models do banco de dados
    │   |   └── xyz_model.py        - classe model da entidade xyz, formato SQLAlchemy
    │   └── schemas                 - schemas para representação dos dados em JSON
    │       └── xyz_schema.py       - classe schema da entidade xyz, formato Pydantic
    ├── tests                       - testes unitários
    ├── main.py                     - Arquivo de configuração e startup do serviço
    └── routes.py                   - arquivos de rotas que conterá os endpoints


A maioria dos diretórios e arquivos do serviço base são internos ao funcionamento e não necessitam alterações. Em seguida é apresentado os principais diretórios e arquivos para desenvolvimento da lógica do serviço.



## Principais arquivos e diretórios

Utilize os seguintes arquivos pra implmentar a lógica do serviço:

* core/config.py - variáveis de configuração neste arquivo

* core/utils.py - funções e classes auxiliares gerais usadas por todo o serviço

* dependencies/ - coloque as classes de lógica, CRUD, acesso e tratamento de dados aqui

* models/domain - Models do SQLAlchemy neste diretório

* models/schemas - Schemas de representação dos dados em JSON nesse diretório, classes padrão Pydantic

* tests/ - testes unitário aqui

* routes.py - rotas dos endpoints aqui



# Desenvolvimento

> Para desenvolvimento local, é aconselhavel rodar o serviço como um container Docker em conjunto com o proxy reverso do Nginx.


## Configuração local

A configuração dos serviços é baseada em *Variáveis de Ambiente*. Utilize a sessão *environment* do arquivo **docker-compose.yml** para definir as variáveis que serão utilizadas pelo container. Exemplo:

```yml
    environment:
      - STAGE=local
      - CLUSTER_URL=http://172.17.0.1:80
      - BUILD_ID=1
      - DEBUG=0
      - DATABASE_URL=mysql+pymysql://root:pass4mysql@172.17.0.1/homolog
```


## Portas e Proxy

Ao rodar localmente, defina um número **único** de porta de saída para o serviço. Esta porta é utilizada posteriormente na configuração do proxy reverso.

```yml
    ports: 
      - "3000:3002" # porta de saída exemplo 3000(única na sua máquina), (3002 padrão não alterar)
      - "9000:8080" # lambda port
      - "5678:5678" # python debug port
```


## Rodando localmente

Utilize os arquivos **Dockerfile.local** e **docker-compose.yml** para criar a imagem do serviço e rodar o container:

1º - Fazer build da imagem, na raiz do projeto
```sh
    $ docker build -t nome_do_service -f Dockerfile.local .
```

2º - Rodar o container
```sh
    $ docker-compose up
```

## Documentação dos endpoints

O framework FastAPI é integrado com o [Swagger](https://swagger.io/). A geração da documentação dos endpoints é gerada automaticamente.

Para ter acesso a documentação do serviço basta acessar [https://url_do_host/stage/nome_servico/docs](https://url_do_host/stage/nome_servico/docs)


# Deploy

O deploy roda pelo arquivo de Pipeline *Jenkinsfile*, baseado no branch/tag que o projeto for enviado.

## Configuração


No aplicativo Jenkins, adicione a variável e o seu valor para determinado stage.

Exemplo, *homolog_envfile* 
```json
"swissre_service" :
{
        "STAGE": "homolog",
        "CLUSTER_URL": "https://meboqxocli.execute-api.us-west-1.amazonaws.com",
        "DATABASE_URL": "mysql+pymysql://root:pass4mysql@172.17.0.1/homolog"
}
```
