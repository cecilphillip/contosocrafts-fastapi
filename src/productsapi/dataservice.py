from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
import asyncio
import os

MAX_PAGE_RETURN = 20

mongo_connection_str = os.environ.get(
    'MONGO_CONNECTION', 'mongodb://admin:admin@localhost:27017')

_client: AsyncIOMotorClient = None
_products_db = None
_products_collection: AsyncIOMotorCollection = None


async def get_products(page: int = 1, limit: int = 20):
    cursor = _products_collection.find().skip((page - 1) * limit).limit(limit)
    results = await cursor.to_list(length=MAX_PAGE_RETURN)
    return results


async def get_product(id: str):
    query = {"Id": id}
    product = await _products_collection.find_one(query)    
    return product


async def update_product_rating(id: str, rating: int):
    query = {"Id": id}
    push = {'$push': {'Ratings': rating}}
    product = await _products_collection.update_one(query, push)    
    


def connect():
    global _client, _products_db, _products_collection
    _client = AsyncIOMotorClient(mongo_connection_str)
    _products_db = _client.contosocrafts
    _products_collection = _products_db.products


def shutdown():
    _client.close()
