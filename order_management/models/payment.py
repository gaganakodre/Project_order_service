from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Payment:
    id: Optional[int]
    invoice_number: str
    product_name: str
    quantity: int
    amount: float
    gst_amount: float
    work_order_number: str
    hsn_number: str
    client_address: str
    payment_terms: str
    dc_number: str
    dc_date: str
    po_number: str
    po_date: str
    created_at: datetime = datetime.now()
    company_name: str = "AEROWAVE TECHNOLOGIES"
    company_address: str = """#14 NO 102 CHINNAGIRIYAPPA ESTATE
NAVILU NAGAR, NEAR NICE ROAD, ANDRALLI
CONTACT NO-9738274553 / 8660024918"""
    company_gst: str = "29ACGFA4296A1ZG"
    company_email: str = "aerowavetechnologies.aw@gmail.com"
    bank_details: str = """Bank Name: SVC BANK
Account No: 300004000006796
IFSC CODE: SVCB0000061"""




