import os

from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.utils import get_openapi
from fastapi.exceptions import RequestValidationError
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.requests import Request
from starlette.exceptions import HTTPException
from mangum import Mangum

from app.core import config
from app.errors.http_error import http_error_handler
from app.errors.validation_erros import http422_error_handler
from app.routes import router as service_routes
from app.routes_dominios import router as domain_routes
from app.core.utils import set_trace

from agristamp_common.dependencies.auth_dependency import auth_required
from agristamp_common.utils.logs import logger

api = APIRouter()

API_TITLE = "SwissRe Service"
API_DESCRIPTION = 'Microserviço para integração a API da SwissRe'


@api.get("/health")
def health(request: Request):
    health_message =  {"result": "health check ok",
                       "version": config.VERSION_STR,
                       "stage": config.STAGE}

    logger.info(health_message)

    return health_message


@api.get("/documentation")
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    if os.getenv('DEV'):
        doc_server = {
            "url": f"http://localhost/{config.STAGE}"
        }
    else:
        doc_server = {
            "url": f"{config.CLUSTER_URL}/{config.STAGE}"
        }

    openapi_schema = get_openapi(
        title=API_TITLE,
        version=config.VERSION_STR,
        description=API_DESCRIPTION,
        routes=app.routes,
        servers=[doc_server],
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(title=API_TITLE,
              description=API_DESCRIPTION,
              openapi_url='/swissre_service/documentation',
              docs_url='/swissre_service/docs',
              root_path=f"/{config.STAGE}")


app.openapi = custom_openapi

app.include_router(api, prefix="/swissre_service")
app.include_router(service_routes, prefix="/swissre_service", dependencies=[Depends(auth_required)])
app.include_router(domain_routes, prefix="/swissre_service", dependencies=[Depends(auth_required)])

app.add_middleware(DBSessionMiddleware, db_url=config.DATABASE_URL)

app.add_exception_handler(HTTPException, http_error_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)


# to make it work with Amazon Lambda
api_gateway_handler = Mangum(app=app)

# debug
if os.getenv('DEBUG') == '1':
    set_trace()
