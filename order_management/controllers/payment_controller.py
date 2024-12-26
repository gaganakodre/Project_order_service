from datetime import datetime
from models.payment import Payment
from utils.rds_helper import RDSHelper
from controllers.order_controller import  OrderController


class PaymentController:
    def __init__(self):
        self.rds = RDSHelper()
        self.order_controller = OrderController()

    def generate_invoice_number(self):
        sql = "SELECT invoice_number FROM payments ORDER BY id DESC LIMIT 1"
        result = self.rds.execute_statement(sql)
        
        if result and result[0]['invoice_number']:
            last_num = int(result[0]['invoice_number'].split('-')[1])
            new_num = str(last_num + 1).zfill(4)
        else:
            new_num = '0001'
            
        return f'INV-{new_num}'

    def create_payment(self, payment: Payment):
        payment.invoice_number = self.generate_invoice_number()
        sql = """
        INSERT INTO payments (
            invoice_number, product_name, quantity, amount,
            gst_amount, work_order_number, hsn_number,dc_number,dc_date,
            po_number,po_date,client_address, payment_terms, company_address,
            bank_details, created_at
        ) VALUES (
            %(invoice_number)s, %(product_name)s, %(quantity)s,
            %(amount)s, %(gst_amount)s, %(work_order_number)s,
            %(hsn_number)s,%(dc_number)s,%(dc_date)s,%(po_number)s,%(po_date)s,
            %(client_address)s, %(payment_terms)s,
            %(company_address)s, %(bank_details)s, %(created_at)s
        ) RETURNING id;
        """
        _, payment_id = self.rds.execute_command_returning_id(sql, vars(payment))
        return payment_id



    
    def get_all_payments(self):
        sql = """
        SELECT 
            id,
            invoice_number,
            product_name,
            quantity,
            amount,
            gst_amount,
            work_order_number,
            hsn_number,
            client_address,
            payment_terms,
            dc_number,
            dc_date,
            po_number,
            po_date,
            created_at
        FROM payments 
        ORDER BY created_at DESC
        """
        return self.rds.execute_statement(sql)

    def get_payment_by_id(self, payment_id):
        sql = """
        SELECT * FROM payments WHERE id = %s
        """
        return self.rds.execute_statement(sql, (payment_id,))[0]
    
    def delete_payment(self, payment_id):
        sql = "DELETE FROM payments WHERE id = %s"
        return self.rds.execute_command(sql, (payment_id,))


