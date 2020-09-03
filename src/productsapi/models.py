from pydantic import BaseModel, Extra
from typing import List


def captialize_alias(val: str) -> str:
    return val.capitalize()


class Product(BaseModel):
    id: str
    maker: str
    image: str
    url: str
    title: str
    description: str
    ratings: List[int]

    class Config:
        allow_population_by_field_name: True
        alias_generator = captialize_alias
