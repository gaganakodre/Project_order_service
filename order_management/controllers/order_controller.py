from utils.rds_helper import RDSHelper
from models.order import Order

class OrderController:
    def __init__(self):
        self.rds = RDSHelper()

    def generate_wo_num(self):
        sql = "SELECT wo_num FROM orders ORDER BY id DESC LIMIT 1"
        result = self.rds.execute_statement(sql)
        
        if result and result[0]['wo_num']:
            # Extract the number part and increment
            last_num = int(result[0]['wo_num'].split('-')[1])
            new_num = str(last_num + 1).zfill(4)
        else:
            # First order
            new_num = '0001'
            
        return f'AWN-{new_num}'

    def create_order(self, order: Order):
        # Generate WO number before creation
        order.wo_num = self.generate_wo_num()
        order.total_amount = order.quantity * order.unit_price
        
        sql = """
        INSERT INTO orders (
            customer_name, product_name, quantity, unit_price, 
            total_amount, status, created_at, wo_num, po_num
        )
        VALUES (
            %(customer_name)s, %(product_name)s, %(quantity)s, 
            %(unit_price)s, %(total_amount)s, %(status)s, 
            %(created_at)s, %(wo_num)s, %(po_num)s
        )
        RETURNING id;
        """
        _, order_id = self.rds.execute_command_returning_id(sql, vars(order))
        return order_id

    def get_all_orders(self):
        sql = "SELECT * FROM orders ORDER BY created_at DESC"
        return self.rds.execute_statement(sql)

    def get_order(self, order_id: int):
        sql = "SELECT * FROM orders WHERE id = %(order_id)s"
        result = self.rds.execute_statement(sql, {"order_id": order_id})
        return result[0] if result else None

    def update_order_status(self, order_id: int, status: str):
        sql = "UPDATE orders SET status = %(status)s WHERE id = %(order_id)s"
        return self.rds.execute_command(sql, {"order_id": order_id, "status": status})

    def delete_order(self, order_id: int):
        sql = "DELETE FROM orders WHERE id = %(order_id)s"
        return self.rds.execute_command(sql, {"order_id": order_id})
