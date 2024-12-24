from flask import Flask, request, jsonify, session, redirect, url_for, render_template
from functools import wraps
from datetime import timedelta
import os
import secrets
from ..controllers.order_controller import OrderController
from ..controllers.login_controller import LoginController
from ..controllers.enquiry_controller import EnquiryController
from ..controllers.payment_controller import PaymentController
from ..controllers.dashboard_controller import DashboardController
from ..models.order import Order
from ..models.login import Login
from ..models.enquiry import Enquiry
from ..models.payment import Payment
from utils.rds_helper import RDSHelper

# Initialize Flask app with configurations
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Initialize controllers
order_controller = OrderController()
login_controller = LoginController()
enquiry_controller = EnquiryController()
payment_controller = PaymentController()
dashboard_controller = DashboardController()

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Route handlers
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'GET':
        return render_template('login.html')
    
    data = request.json
    user = login_controller.authenticate_user(
        email=data['email'],
        password=data['password']
    )
    
    if user:
        session['user_id'] = user['id']
        session['email'] = user['email']
        session.permanent = True
        return jsonify({'success': True, 'redirect': url_for('dashboard')})
    
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    
    data = request.json
    if login_controller.get_user_by_email(data['email']):
        return jsonify({'success': False, 'message': 'Email already registered'}), 400
    
    user = Login(
        user_name=data['user_name'],
        email=data['email'],
        password=data['password']
    )
    user_id = login_controller.create_user(user)
    return jsonify({'success': True, 'user_id': user_id}), 201

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/dashboard-data')
@login_required
def dashboard_data():
    return jsonify(dashboard_controller.get_dashboard_data())

# Order routes
@app.route('/orders', methods=['POST'])
@login_required
def create_order():
    data = request.json
    order = Order(
        id=None,
        customer_name=data['customer_name'],
        product_name=data['product_name'],
        quantity=data['quantity'],
        unit_price=data['unit_price'],
        total_amount=data['quantity'] * data['unit_price'],
        status='PENDING',
        po_num=data["po_num"]
    )
    order_id = order_controller.create_order(order)
    return jsonify({'order_id': order_id}), 201

@app.route('/orders', methods=['GET'])
@login_required
def get_orders():
    orders = order_controller.get_all_orders()
    return jsonify(orders)

@app.route('/orders/<int:order_id>', methods=['GET'])
@login_required
def get_order(order_id):
    order = order_controller.get_order(order_id)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders/<int:order_id>/status', methods=['PUT'])
@login_required
def update_order_status(order_id):
    data = request.json
    rows_affected = order_controller.update_order_status(order_id, data['status'])
    if rows_affected:
        return jsonify({'message': 'Order updated successfully'})
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    rows_affected = order_controller.delete_order(order_id)
    if rows_affected:
        return jsonify({'message': 'Order deleted successfully'})
    return jsonify({'error': 'Order not found'}), 404

# Navigation routes
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/order_list')
@login_required
def order_list():
    return render_template('order_list.html')


@app.route('/create_order')
@login_required
def create_order_page():
    return render_template('index.html')

# Enquiry routes
@app.route('/enquiry_form')
@login_required
def enquiry_form():
    return render_template('enquiry_form.html')

@app.route('/enquiry_list')
@login_required
def enquiry_list():
    return render_template('enquiry_list.html')

@app.route('/enquiries/<int:id>', methods=['DELETE'])
@login_required
def delete_enquiry(id):
    try:
        sql = "DELETE FROM enquiries WHERE id = %s"
        RDSHelper().execute_command(sql, (id,))
        return jsonify({"message": "Enquiry deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/enquiries/<int:id>/status', methods=['PUT'])
@login_required
def update_enquiry_status(id):
    data = request.json
    sql = """
    UPDATE enquiries 
    SET enquiry_status = %s 
    WHERE id = %s
    """
    RDSHelper().execute_command(sql, (data['status'], id))
    return jsonify({"message": "Status updated successfully"})

@app.route('/print_enquiry/<int:enquiry_id>')
@login_required
def print_enquiry(enquiry_id):
    sql = """
    SELECT * FROM enquiries 
    WHERE id = %s
    """
    result = RDSHelper().execute_statement(sql, (enquiry_id,))
    enquiry = result[0] if result else None
    return render_template('print_enquiry.html', enquiry=enquiry)


@app.route('/enquiries', methods=['POST'])
@login_required
def create_enquiry():
    data = request.json
    enquiry = Enquiry(
        id=None,
        enquiry_id=None,
        client_name=data['client_name'],
        drawing_number=data['drawing_number'],
        part_number=data['part_number'],
        part_revision_number=data['part_revision_number'],
        material_type=data['material_type'],
        material_spec=data['material_spec'],
        with_material=data['with_material'],
        unit_price=float(data['unit_price']),
        quantity=int(data['quantity']),
        total_price=float(data['total_price']),
        remarks=data['remarks'],
        enquiry_status='PENDING',
        address_details=data['address_details']
    )
    enquiry_id = enquiry_controller.create_enquiry(enquiry)
    return jsonify({'enquiry_id': enquiry_id}), 201

@app.route('/enquiries', methods=['GET'])
@login_required
def get_enquiries():
    enquiries = enquiry_controller.get_all_enquiries()
    return jsonify(enquiries)

@app.route('/clients', methods=['GET'])
@login_required
def get_clients():
    clients = enquiry_controller.get_client_names()
    return jsonify(clients)

# Payment routes
@app.route('/payment_form')
@login_required
def payment_form():
    return render_template('payment_form.html')

@app.route('/payments', methods=['GET', 'POST'])
@login_required
def payments():
    if request.method == 'POST':
        data = request.json
        payment = Payment(
            id=None,
            invoice_number=None,
            product_name=data['product_name'],
            quantity=data['quantity'],
            amount=data['amount'],
            gst_amount=data['gst_amount'],
            work_order_number=data['work_order_number'],
            hsn_number=data['hsn_number'],
            client_address=data['client_address'],
            payment_terms=data['payment_terms'],
            dc_number=data['dc_number'],
            dc_date=data['dc_date'],
            po_number=data['po_number'],
            po_date=data['po_date']
        )
        print(payment,'pppppppppayment')
        payment_id = payment_controller.create_payment(payment)
        return jsonify({'payment_id': payment_id}), 201
    
    payments = payment_controller.get_all_payments()
    return jsonify(payments)

@app.route('/payment_list')
@login_required
def payment_list():
    return render_template('payment_list.html')

@app.route('/print_invoice/<int:payment_id>')
@login_required
def print_invoice(payment_id):
    payment = payment_controller.get_payment_by_id(payment_id)
    return render_template('print_invoice.html', payment=payment)

@app.route('/payments/<int:payment_id>', methods=['DELETE'])
@login_required
def delete_payment(payment_id):
    payment_controller.delete_payment(payment_id)
    return jsonify({'message': 'Payment deleted successfully'}), 200


@app.route('/order_products', methods=['GET'])
@login_required
def get_order_products():
    sql = """
    SELECT DISTINCT o.id, o.product_name, o.quantity, o.total_amount, o.wo_num 
    FROM orders o 
    WHERE o.status = 'COMPLETED' 
    AND NOT EXISTS (
        SELECT 1 FROM payments p 
        WHERE p.work_order_number = o.wo_num
    )
    """
    products = RDSHelper().execute_statement(sql)
    return jsonify(products)

@app.route("/order_details")
def get_order_details():
    sql = """
    SELECT 
        id, product_name, quantity, total_amount, wo_num
    FROM orders 
    WHERE status = 'COMPLETED' ;
    
    """
    details = RDSHelper().execute_statement(sql)
    print("Orders fetched:", details)  # Debug log
    return jsonify(details)





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
