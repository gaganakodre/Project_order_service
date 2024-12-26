from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Enquiry:
    id: Optional[int]
    enquiry_id: str
    client_name: str
    drawing_number: str
    part_number: str
    part_revision_number: str
    material_type: str
    material_spec: str
    with_material: bool
    unit_price: float
    quantity: int
    total_price: float
    remarks: str
    address_details: str
    enquiry_status: str = 'PENDING'    
    enquiry_date: datetime = datetime.now()
    
