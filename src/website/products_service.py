from models import Product
from http import HTTPStatus
from socket import AF_INET
from typing import Dict, Any

import asyncio

import aiohttp
from aiohttp.client import ClientResponse

_AIOHTTP_HOST_LIMIT = 40
_DAPR_BASE = 'http://localhost:3500'
_BASE_PRODUCTS_ENDPOINT = '/v1.0/invoke/productsapi/method/products'
_BASE_STATE_ENDPOINT = '/v1.0/state/statestore'
_BASE_PUBSUB_ENDPOINT = '/v1.0/publish/rabbitmqbus'


class ProductService():
    aio_client: aiohttp.ClientSession = None

    @classmethod
    def get_aio_client(cls) -> aiohttp.ClientSession:
        if cls.aio_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                ttl_dns_cache=100, family=AF_INET, limit_per_host=_AIOHTTP_HOST_LIMIT)
            cls.aio_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector)

        return cls.aio_client

    @classmethod
    async def close_aio_client(cls):
        if cls.aio_client:
            await cls.aio_client.close()
            cls.aio_client = None

    @classmethod
    async def get_products(cls, page: int = 1, limit: int = 20):
        client = cls.get_aio_client()
        resp = await client.get(f'{_DAPR_BASE}{_BASE_PRODUCTS_ENDPOINT}')
        # I should put some error handling here or something
        payload = await resp.json()
        product_list = [Product.parse_obj(product) for product in payload]
        return product_list

    @classmethod
    async def get_product(cls, id: str) -> Product:
        client = cls.get_aio_client()
        resp = await client.get(f'{_DAPR_BASE}{_BASE_PRODUCTS_ENDPOINT}/{id}')

        payload = await resp.json()
        product = Product.parse_obj(payload)
        return product


class StateService():
    aio_client: aiohttp.ClientSession = None

    @classmethod
    def get_aio_client(cls) -> aiohttp.ClientSession:
        if cls.aio_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                ttl_dns_cache=100, family=AF_INET, limit_per_host=_AIOHTTP_HOST_LIMIT)
            cls.aio_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector)

        return cls.aio_client

    @classmethod
    async def close_aio_client(cls):
        if cls.aio_client:
            await cls.aio_client.close()
            cls.aio_client = None

    @classmethod
    async def add_to_cart(cls, product: Product):
        client = cls.get_aio_client()
        resp: ClientResponse = await client.get(f'{_DAPR_BASE}{_BASE_STATE_ENDPOINT}/cart')

        if resp.status not in [HTTPStatus.OK, HTTPStatus.NO_CONTENT]:
            return

        state: Dict[str, Any] = {}
        if resp.status == HTTPStatus.NO_CONTENT:
            state[product.id] = {'title': product.title, 'quantity': 1}

        if resp.status == HTTPStatus.OK:
            state: Dict = await resp.json()
            if product.id in state:
                quantity: int = state[product.id]['quantity']
                state[product.id]['quantity'] = quantity + 1
            else:
                state[product.id] = {'title': product.title, 'quantity': 1}

        # I should probably log here too
        await client.post(f'{_DAPR_BASE}{_BASE_STATE_ENDPOINT}/', json=[{'key': "cart", 'value': state}])

    @classmethod
    async def get_cart_state(cls) -> Dict[str, Any]:
        client = cls.get_aio_client()
        resp: ClientResponse = await client.get(f'{_DAPR_BASE}{_BASE_STATE_ENDPOINT}/cart')

        if resp.status != HTTPStatus.OK:
            return None

        state: [str, Any] = await resp.json()
        return state

    @classmethod
    async def clear_cart_state(cls):
        client = cls.get_aio_client()
        resp: ClientResponse = await client.delete(f'{_DAPR_BASE}{_BASE_STATE_ENDPOINT}/cart')

        if resp.status == HTTPStatus.OK:
            print('state cleared')
        else:
            print('state not cleared')


class PubSubService():
    aio_client: aiohttp.ClientSession = None

    @classmethod
    def get_aio_client(cls) -> aiohttp.ClientSession:
        if cls.aio_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(
                ttl_dns_cache=100, family=AF_INET, limit_per_host=_AIOHTTP_HOST_LIMIT)
            cls.aio_client = aiohttp.ClientSession(
                timeout=timeout, connector=connector)

        return cls.aio_client

    @classmethod
    async def close_aio_client(cls):
        if cls.aio_client:
            await cls.aio_client.close()
            cls.aio_client = None

    @classmethod
    async def publish_message(cls, topic: str, data: dict):
        client = cls.get_aio_client()
        resp: ClientResponse = await client.post(f'{_DAPR_BASE}{_BASE_PUBSUB_ENDPOINT}/{topic}', json=data)
        if resp.status == HTTPStatus.OK:
            await StateService.clear_cart_state()
