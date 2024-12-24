from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Order:
    id: Optional[int]
    customer_name: str
    product_name: str
    quantity: int
    unit_price: float
    total_amount: float
    status: str
    po_num: str
    created_at: datetime = datetime.now()
    wo_num: Optional[str] = None
