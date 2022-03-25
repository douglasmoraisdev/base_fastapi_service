import os
from tempfile import NamedTemporaryFile
from fastapi import File, UploadFile
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

from app.db.mongo import mapas_collection
from app.models.schemas.mapas_schema import TalhaoCreate
from app.core import config
from agristamp_common.utils import s3storage

BUCKET_NAME = config.SERVICE_SLUG.replace('_', '-')

async def get_talhao_by_id(id: str) -> dict:
    talhao = await mapas_collection.find_one({"_id": ObjectId(id)})
    if talhao:
        talhao['_id'] = str(talhao['_id'])
        return talhao


async def get_all_talhoes():
    talhoes = []
    async for talhao in mapas_collection.find():
        talhao['_id'] = str(talhao['_id'])
        talhoes.append(talhao)

    return {'result': talhoes, 'total': 99}


async def insert_talhao(talhao_data: TalhaoCreate) -> dict:
    talhao = await mapas_collection.insert_one(dict(talhao_data))
    new_talhao = await mapas_collection.find_one(
        {"_id": ObjectId(talhao.inserted_id)}
    )
    new_talhao["_id"] = str(new_talhao['_id'])

    return new_talhao


async def update_talhao(id: str, talhao_data: dict):

    # Pega somente os campos com valor
    data = {k: v for k, v in talhao_data.items() if v is not None}

    if len(data) < 1:
        return False
    talhao = await mapas_collection.find_one({"_id": ObjectId(id)})
    if talhao:
        new_talhao = await mapas_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if new_talhao:
            new_talhao = await mapas_collection.find_one({"_id": ObjectId(id)})
            new_talhao['_id'] = str(new_talhao['_id'])

            return new_talhao

    return None


async def upload_mapa_file(file: UploadFile = File(...)):

    return_obj = s3storage.upload_fastapi_uploadfile(file, 'mapas', BUCKET_NAME)

    return return_obj
