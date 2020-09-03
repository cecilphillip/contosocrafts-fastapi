from fastapi import FastAPI, Body, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from pydantic.dataclasses import dataclass
from starlette.responses import JSONResponse, Response

from typing import Optional, Union
from http import HTTPStatus
import socket
import platform
import logging

import dataservice
from models import Product

extra = {'host_name': socket.gethostname(), 'system': platform.uname()[0]}
log_format = f' %(levelname)s:  {extra["system"]} {extra["host_name"]} - %(asctime)s - %(name)s - %(funcName)s - %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

api = FastAPI()


@api.get('/products')
async def get_product_list(page: int = 1, limit: int = 20):
    logging.info('Querying database for products')
    products = await dataservice.get_products(page, limit)

    logging.info('Parsing dict response into model')
    results = [Product.parse_obj(p) for p in products]
    content = jsonable_encoder(results, by_alias=False)
    return JSONResponse(content=content)


@api.get('/products/{id}')
async def get_product_by_id(id: str):
    logging.info(f'Querying database for product {id}')
    product = await dataservice.get_product(id)

    logging.info('Parsing dict response into model')
    result = Product.parse_obj(product)
    content = jsonable_encoder(result, by_alias=False)
    return JSONResponse(content=content)


@api.patch('/products/{id}')
async def update_product_rating(id: str, rating: int = Body(..., embed=True)):
    logging.info('Updating product {id} in database')
    await dataservice.update_product_rating(id, rating)
    return Response(status_code=HTTPStatus.CREATED)


def boot():
    dataservice.connect()


def shutdown():
    dataservice.shutdown()


api.add_event_handler("startup", boot)
api.add_event_handler("shutdown", shutdown)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(api, host='0.0.0.0', port=8000)
