CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    wo_num VARCHAR(20) UNIQUE,
    po_num VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS enquiries (
    id SERIAL PRIMARY KEY,
    enquiry_id VARCHAR(20) UNIQUE NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    drawing_number VARCHAR(50) NOT NULL,
    part_number VARCHAR(50) NOT NULL,
    part_revision_number VARCHAR(50) NOT NULL,
    material_type VARCHAR(100) NOT NULL,
    material_spec VARCHAR(100) NOT NULL,
    with_material BOOLEAN NOT NULL,
    enquiry_date TIMESTAMP NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    remarks TEXT,
    enquiry_status VARCHAR(50) NOT NULL,
    address_details TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    invoice_number VARCHAR(20) UNIQUE NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    quantity INTEGER NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    gst_amount DECIMAL(10,2) NOT NULL,
    work_order_number VARCHAR(20) NOT NULL,
    hsn_number VARCHAR(50) NOT NULL,
    client_address TEXT NOT NULL,
    payment_terms VARCHAR(50) NOT NULL,
    company_address TEXT NOT NULL,
    bank_details TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL
);


ALTER TABLE public.payments 
ADD COLUMN dc_number VARCHAR,
ADD COLUMN dc_date TIMESTAMP,
ADD COLUMN po_number VARCHAR,
ADD COLUMN po_date TIMESTAMP;