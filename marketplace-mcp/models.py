from pydantic import BaseModel
from typing import List, Optional

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

class MarketplaceSeller(BaseModel):
    id: int
    name: str
    rating: float
    baseDeliveryDays: int

class MarketplaceOffer(BaseModel):
    id: int
    product: Product
    seller: MarketplaceSeller
    price: float
    stockQuantity: int
    shippingFee: float
    deliveryTimeDays: int

class MarketplacePurchaseDraftItem(BaseModel):
    id: int
    product: Product
    quantity: int
    seller: MarketplaceSeller
    price: float
    shippingFee: float
    deliveryTimeDays: int

class MarketplacePurchaseDraft(BaseModel):
    id: int
    totalCost: float
    status: str
    items: List[MarketplacePurchaseDraftItem]

class MarketplaceOrderItem(BaseModel):
    id: int
    product: Product
    quantity: int
    seller: MarketplaceSeller
    price: float
    shippingFee: float
    deliveryTimeDays: int

class MarketplaceOrder(BaseModel):
    id: int
    draftId: int
    totalCost: float
    status: str
    createdAt: str
    expectedDeliveryDate: str
    items: List[MarketplaceOrderItem]
