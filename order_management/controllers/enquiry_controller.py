from datetime import datetime
from models.enquiry import Enquiry
from utils.rds_helper import RDSHelper

class EnquiryController:
    def __init__(self):
        self.rds = RDSHelper()

    def generate_enquiry_id(self):
        sql = "SELECT enquiry_id FROM enquiries ORDER BY id DESC LIMIT 1"
        result = self.rds.execute_statement(sql)
        
        if result and result[0]['enquiry_id']:
            last_num = int(result[0]['enquiry_id'].split('-')[1])
            new_num = str(last_num + 1).zfill(4)
        else:
            new_num = '0001'
            
        return f'ENQ-{new_num}'

    def create_enquiry(self, enquiry: Enquiry):
        enquiry.enquiry_id = self.generate_enquiry_id()
        sql = """
        INSERT INTO enquiries (
            enquiry_id, client_name, drawing_number, part_number,
            part_revision_number, material_type, material_spec,
            with_material, enquiry_date, unit_price, quantity,
            total_price, remarks, enquiry_status, address_details
        ) VALUES (
            %(enquiry_id)s, %(client_name)s, %(drawing_number)s,
            %(part_number)s, %(part_revision_number)s, %(material_type)s,
            %(material_spec)s, %(with_material)s, %(enquiry_date)s,
            %(unit_price)s, %(quantity)s, %(total_price)s,
            %(remarks)s, %(enquiry_status)s, %(address_details)s
        ) RETURNING id;
        """
        _, enquiry_id = self.rds.execute_command_returning_id(sql, vars(enquiry))
        return enquiry_id

    def get_all_enquiries(self):
        sql = "SELECT * FROM enquiries ORDER BY enquiry_date DESC"
        return self.rds.execute_statement(sql)

    def get_client_names(self):
        sql = "SELECT DISTINCT customer_name FROM orders"
        return self.rds.execute_statement(sql)

    def update_enquiry_status(self, enquiry_id: int, status: str):
        sql = "UPDATE enquiries SET enquiry_status = %(status)s WHERE id = %(enquiry_id)s"
        return self.rds.execute_command(sql, {"enquiry_id": enquiry_id, "status": status})

    def get_enquiry(self, enquiry_id: int):
        sql = "SELECT * FROM enquiries WHERE id = %(enquiry_id)s"
        result = self.rds.execute_statement(sql, {"enquiry_id": enquiry_id})
        return result[0] if result else None
