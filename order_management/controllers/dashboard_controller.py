from ..utils.rds_helper import RDSHelper
import logging

class DashboardController:
    def get_dashboard_data(self):
        try:
            total_stats = self.get_total_stats()
            pending_orders = self.get_pending_orders()
            monthly_revenue = self.get_monthly_revenue()
            revenue_chart = self.get_revenue_chart_data()
            products_chart = self.get_products_chart_data()
            recent_invoices = self.get_recent_invoices()
            print(recent_invoices,'pppppppppp')
            return {
                "totalInvoices": total_stats['total_invoices'],
                "totalRevenue": float(total_stats['total_revenue']),
                "pendingOrders": pending_orders['pending_orders'],
                "monthlyRevenue": float(monthly_revenue),
                "revenueChart": revenue_chart,
                "productsChart": products_chart,
                "recentInvoices": recent_invoices
            }
        except Exception as e:
            logging.error(f"Error in get_dashboard_data: {str(e)}")
            return self.get_default_data()

    def get_total_stats(self):
        sql = """
        SELECT 
            COALESCE(COUNT(*), 0) as total_invoices,
            COALESCE(SUM(amount + gst_amount), 0) as total_revenue
        FROM payments
        """
        result = RDSHelper().execute_statement(sql)
        return result[0] if result else {'total_invoices': 0, 'total_revenue': 0}

    def get_pending_orders(self):
        sql = """
        SELECT COALESCE(COUNT(*), 0) as pending_orders
        FROM orders 
        WHERE status = 'COMPLETED' 
        AND NOT EXISTS (
            SELECT 1 FROM payments p 
            WHERE p.work_order_number = orders.wo_num
        )
        """
        result = RDSHelper().execute_statement(sql)
        return result[0] if result else {'pending_orders': 0}

    def get_monthly_revenue(self):
        sql = """
        SELECT COALESCE(SUM(amount + gst_amount), 0) as monthly_revenue
        FROM payments
        WHERE EXTRACT(MONTH FROM created_at) = EXTRACT(MONTH FROM CURRENT_DATE)
        AND EXTRACT(YEAR FROM created_at) = EXTRACT(YEAR FROM CURRENT_DATE)
        """
        result = RDSHelper().execute_statement(sql)
        return result[0]['monthly_revenue'] if result else 0

    def get_revenue_chart_data(self):
        sql = """
        SELECT 
            TO_CHAR(created_at, 'Month') as month,
            SUM(amount + gst_amount) as revenue
        FROM payments
        WHERE created_at >= CURRENT_DATE - INTERVAL '6 months'
        GROUP BY TO_CHAR(created_at, 'Month')
        ORDER BY MIN(created_at)
        """
        result = RDSHelper().execute_statement(sql)
        return {
            'labels': [r['month'].strip() for r in result],
            'data': [float(r['revenue']) for r in result]
        }

    def get_products_chart_data(self):
        sql = """
        SELECT 
            product_name,
            COUNT(*) as count
        FROM orders
        GROUP BY product_name
        ORDER BY count DESC
        LIMIT 5
        """
        result = RDSHelper().execute_statement(sql)
        return {
            'labels': [r['product_name'] for r in result],
            'data': [int(r['count']) for r in result]
        }

    def get_recent_invoices(self):
        sql = """
        SELECT 
            invoice_number,
            product_name,
            amount + gst_amount as amount,
            created_at
        FROM payments
        ORDER BY created_at DESC
        LIMIT 5
        """
        return RDSHelper().execute_statement(sql)

    def get_default_data(self):
        return {
            "totalInvoices": 0,
            "totalRevenue": 0,
            "pendingOrders": 0,
            "monthlyRevenue": 0,
            "revenueChart": {"labels": [], "data": []},
            "productsChart": {"labels": [], "data": []},
            "recentInvoices": []
        }
