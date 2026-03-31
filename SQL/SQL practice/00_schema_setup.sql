-- =============================================================================
-- SQL Practice Database Schema Setup
-- Database: local_db (PostgreSQL)
-- Connection: postgresql://sanket@localhost:5432/local_db
-- 
-- This script creates a realistic e-commerce company database for SQL practice.
-- Run this FIRST before attempting any practice questions.
-- =============================================================================

-- Clean up existing tables (in dependency order)
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS reviews CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS employee_projects CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS salary_history CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS shipping_addresses CASCADE;

-- =============================================================================
-- DDL: Table Definitions
-- =============================================================================

-- 1. Departments
CREATE TABLE departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    location VARCHAR(100),
    budget NUMERIC(12, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Employees
CREATE TABLE employees (
    emp_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    hire_date DATE NOT NULL,
    job_title VARCHAR(100),
    salary NUMERIC(10, 2),
    commission_pct NUMERIC(4, 2),
    manager_id INT REFERENCES employees(emp_id),
    dept_id INT REFERENCES departments(dept_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_employees_dept ON employees(dept_id);
CREATE INDEX idx_employees_manager ON employees(manager_id);
CREATE INDEX idx_employees_hire_date ON employees(hire_date);

-- 3. Salary History
CREATE TABLE salary_history (
    history_id SERIAL PRIMARY KEY,
    emp_id INT REFERENCES employees(emp_id),
    old_salary NUMERIC(10, 2),
    new_salary NUMERIC(10, 2),
    change_date DATE NOT NULL,
    change_reason VARCHAR(100)
);

-- 4. Projects
CREATE TABLE projects (
    project_id SERIAL PRIMARY KEY,
    project_name VARCHAR(150) NOT NULL,
    start_date DATE,
    end_date DATE,
    budget NUMERIC(12, 2),
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'on_hold', 'cancelled')),
    dept_id INT REFERENCES departments(dept_id)
);

-- 5. Employee-Project Assignment (Many-to-Many)
CREATE TABLE employee_projects (
    emp_id INT REFERENCES employees(emp_id),
    project_id INT REFERENCES projects(project_id),
    role VARCHAR(50),
    hours_worked NUMERIC(6, 2) DEFAULT 0,
    assigned_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (emp_id, project_id)
);

-- 6. Categories
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INT REFERENCES categories(category_id),
    description TEXT
);

-- 7. Suppliers
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    company_name VARCHAR(150) NOT NULL,
    contact_name VARCHAR(100),
    contact_email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(100),
    country VARCHAR(100),
    rating NUMERIC(3, 2) CHECK (rating >= 0 AND rating <= 5)
);

-- 8. Products
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    category_id INT REFERENCES categories(category_id),
    supplier_id INT REFERENCES suppliers(supplier_id),
    unit_price NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    cost_price NUMERIC(10, 2) CHECK (cost_price >= 0),
    units_in_stock INT DEFAULT 0,
    units_on_order INT DEFAULT 0,
    reorder_level INT DEFAULT 10,
    discontinued BOOLEAN DEFAULT FALSE,
    weight_kg NUMERIC(6, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_supplier ON products(supplier_id);
CREATE INDEX idx_products_price ON products(unit_price);

-- 9. Customers
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(50),
    country VARCHAR(100) DEFAULT 'India',
    registration_date DATE DEFAULT CURRENT_DATE,
    is_premium BOOLEAN DEFAULT FALSE,
    credit_limit NUMERIC(10, 2) DEFAULT 50000.00
);

CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_email ON customers(email);

-- 10. Shipping Addresses
CREATE TABLE shipping_addresses (
    address_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    address_line1 VARCHAR(200) NOT NULL,
    address_line2 VARCHAR(200),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    is_default BOOLEAN DEFAULT FALSE
);

-- 11. Orders
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_date TIMESTAMP,
    delivered_date TIMESTAMP,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned')),
    payment_method VARCHAR(30),
    shipping_cost NUMERIC(8, 2) DEFAULT 0,
    discount_pct NUMERIC(4, 2) DEFAULT 0,
    notes TEXT
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(status);

-- 12. Order Items
CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,
    discount NUMERIC(4, 2) DEFAULT 0
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);

-- 13. Reviews
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    customer_id INT REFERENCES customers(customer_id),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    UNIQUE(product_id, customer_id)
);

-- 14. Inventory Log (for tracking stock changes)
CREATE TABLE inventory (
    log_id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(product_id),
    change_qty INT NOT NULL,
    change_type VARCHAR(20) CHECK (change_type IN ('restock', 'sale', 'return', 'adjustment', 'damaged')),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

SELECT 'Schema created successfully!' AS status;
