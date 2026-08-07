from pydantic import BaseModel
from typing import Optional

class Category(BaseModel):
    id: int
    name: str

class Subcategory(BaseModel):
    id: int
    category: Category
    name: str

class Brand(BaseModel):
    id: int
    name: str

class Model(BaseModel):
    id: int
    brand: Brand
    name: str

class Product(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str] = None
    subcategory: Optional[Subcategory] = None
    model: Optional[Model] = None
    stockQuantity: int
    minimumStock: int
    targetStock: int
    warehouseInfo: Optional[str] = None

class IncomingOrder(BaseModel):
    id: int
    product: Product
    quantity: int
    status: str
    expectedDeliveryDate: Optional[str] = None
    createdAt: str

class Replenishment(BaseModel):
    productId: int
    sku: str
    productName: str
    categoryName: Optional[str] = None
    stockQuantity: int
    minimumStock: int
    targetStock: int
    pendingIncomingQuantity: int
    replenishmentQuantityNeeded: int
