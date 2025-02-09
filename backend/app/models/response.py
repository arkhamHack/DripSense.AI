from pydantic import BaseModel
from typing import List, Dict

class Product(BaseModel):
    name: str
    price: float
    brand: str
    details: Dict[str, str]

class SearchResponse(BaseModel):
    products: List[Product]
    message: str
