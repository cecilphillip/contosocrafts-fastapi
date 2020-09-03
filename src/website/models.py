from pydantic import BaseModel, Extra
from typing import List

class Product(BaseModel):
    id: str
    maker: str
    image: str
    url: str
    title: str
    description: str
    ratings: List[int] = []