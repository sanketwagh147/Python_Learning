-- =============================================================================
-- Dummy Data for SQL Practice
-- Run this AFTER 00_schema_setup.sql
-- =============================================================================

-- ===================== DEPARTMENTS =====================
INSERT INTO departments (dept_name, location, budget) VALUES
('Engineering', 'Bangalore', 5000000.00),
('Marketing', 'Mumbai', 2000000.00),
('Sales', 'Delhi', 3000000.00),
('Human Resources', 'Bangalore', 1500000.00),
('Finance', 'Mumbai', 2500000.00),
('Operations', 'Pune', 1800000.00),
('Customer Support', 'Hyderabad', 1200000.00),
('Research & Development', 'Bangalore', 4500000.00),
('Legal', 'Delhi', 1000000.00),
('Product Management', 'Bangalore', 2200000.00);

-- ===================== EMPLOYEES =====================
-- Managers first (no manager_id)
INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, salary, commission_pct, manager_id, dept_id, is_active) VALUES
('Rajesh', 'Kumar', 'rajesh.kumar@company.com', '9876543210', '2018-03-15', 'VP Engineering', 250000.00, NULL, NULL, 1, TRUE),
('Priya', 'Sharma', 'priya.sharma@company.com', '9876543211', '2018-05-20', 'Marketing Director', 200000.00, 0.05, NULL, 2, TRUE),
('Amit', 'Patel', 'amit.patel@company.com', '9876543212', '2017-11-01', 'Sales Director', 220000.00, 0.10, NULL, 3, TRUE),
('Sunita', 'Reddy', 'sunita.reddy@company.com', '9876543213', '2019-01-10', 'HR Director', 180000.00, NULL, NULL, 4, TRUE),
('Vikram', 'Singh', 'vikram.singh@company.com', '9876543214', '2018-07-25', 'CFO', 280000.00, NULL, NULL, 5, TRUE);

-- Mid-level employees
INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, salary, commission_pct, manager_id, dept_id, is_active) VALUES
('Neha', 'Gupta', 'neha.gupta@company.com', '9876543215', '2019-06-15', 'Senior Software Engineer', 150000.00, NULL, 1, 1, TRUE),
('Arjun', 'Mishra', 'arjun.mishra@company.com', '9876543216', '2019-09-01', 'Senior Software Engineer', 145000.00, NULL, 1, 1, TRUE),
('Kavita', 'Joshi', 'kavita.joshi@company.com', '9876543217', '2020-01-20', 'Marketing Manager', 120000.00, 0.03, 2, 2, TRUE),
('Ravi', 'Verma', 'ravi.verma@company.com', '9876543218', '2019-11-15', 'Sales Manager', 130000.00, 0.08, 3, 3, TRUE),
('Deepa', 'Nair', 'deepa.nair@company.com', '9876543219', '2020-03-10', 'HR Manager', 110000.00, NULL, 4, 4, TRUE),
('Suresh', 'Iyer', 'suresh.iyer@company.com', '9876543220', '2020-02-01', 'Finance Manager', 135000.00, NULL, 5, 5, TRUE),
('Meera', 'Chopra', 'meera.chopra@company.com', '9876543221', '2019-08-20', 'Tech Lead', 160000.00, NULL, 1, 1, TRUE),
('Anil', 'Rao', 'anil.rao@company.com', '9876543222', '2020-06-15', 'Operations Manager', 115000.00, NULL, NULL, 6, TRUE),
('Pooja', 'Desai', 'pooja.desai@company.com', '9876543223', '2020-04-01', 'Support Manager', 105000.00, NULL, NULL, 7, TRUE),
('Karthik', 'Menon', 'karthik.menon@company.com', '9876543224', '2019-12-01', 'R&D Lead', 170000.00, NULL, 1, 8, TRUE);

-- Junior employees
INSERT INTO employees (first_name, last_name, email, phone, hire_date, job_title, salary, commission_pct, manager_id, dept_id, is_active) VALUES
('Sanjay', 'Tiwari', 'sanjay.tiwari@company.com', '9876543225', '2021-01-15', 'Software Engineer', 85000.00, NULL, 6, 1, TRUE),
('Ananya', 'Das', 'ananya.das@company.com', '9876543226', '2021-03-20', 'Software Engineer', 82000.00, NULL, 7, 1, TRUE),
('Rohit', 'Saxena', 'rohit.saxena@company.com', '9876543227', '2021-06-01', 'Junior Developer', 65000.00, NULL, 12, 1, TRUE),
('Divya', 'Pillai', 'divya.pillai@company.com', '9876543228', '2021-02-15', 'Marketing Executive', 60000.00, 0.02, 8, 2, TRUE),
('Manish', 'Agarwal', 'manish.agarwal@company.com', '9876543229', '2021-04-10', 'Sales Executive', 55000.00, 0.12, 9, 3, TRUE),
('Shreya', 'Bhatt', 'shreya.bhatt@company.com', '9876543230', '2021-07-01', 'Sales Executive', 58000.00, 0.10, 9, 3, TRUE),
('Nikhil', 'Kapoor', 'nikhil.kapoor@company.com', '9876543231', '2021-05-15', 'HR Executive', 52000.00, NULL, 10, 4, TRUE),
('Swati', 'Pandey', 'swati.pandey@company.com', '9876543232', '2021-08-20', 'Junior Accountant', 50000.00, NULL, 11, 5, TRUE),
('Rahul', 'Mehta', 'rahul.mehta@company.com', '9876543233', '2022-01-10', 'Intern', 25000.00, NULL, 6, 1, TRUE),
('Priyanka', 'Kulkarni', 'priyanka.kulkarni@company.com', '9876543234', '2022-02-15', 'Data Analyst', 75000.00, NULL, 15, 8, TRUE),
('Arun', 'Srinivasan', 'arun.srinivasan@company.com', '9876543235', '2020-09-01', 'DevOps Engineer', 120000.00, NULL, 1, 1, TRUE),
('Lakshmi', 'Venkatesh', 'lakshmi.venkatesh@company.com', '9876543236', '2021-11-15', 'Product Manager', 140000.00, NULL, NULL, 10, TRUE),
('Prakash', 'Jain', 'prakash.jain@company.com', '9876543237', '2020-10-01', 'Legal Counsel', 130000.00, NULL, NULL, 9, TRUE),
('Geeta', 'Malhotra', 'geeta.malhotra@company.com', '9876543238', '2022-03-01', 'Support Executive', 48000.00, NULL, 14, 7, TRUE),
('Vijay', 'Chauhan', 'vijay.chauhan@company.com', '9876543239', '2022-06-15', 'Junior Developer', 60000.00, NULL, 12, 1, FALSE),
('Anjali', 'Mukherjee', 'anjali.mukherjee@company.com', '9876543240', '2023-01-10', 'Software Engineer', 90000.00, NULL, 12, 1, TRUE),
('Dinesh', 'Yadav', 'dinesh.yadav@company.com', '9876543241', '2023-03-15', 'Marketing Analyst', 70000.00, 0.02, 8, 2, TRUE);

-- ===================== SALARY HISTORY =====================
INSERT INTO salary_history (emp_id, old_salary, new_salary, change_date, change_reason) VALUES
(1, 200000.00, 220000.00, '2019-04-01', 'Annual Increment'),
(1, 220000.00, 250000.00, '2020-04-01', 'Promotion'),
(6, 100000.00, 120000.00, '2020-04-01', 'Annual Increment'),
(6, 120000.00, 150000.00, '2021-04-01', 'Promotion'),
(7, 110000.00, 130000.00, '2020-04-01', 'Annual Increment'),
(7, 130000.00, 145000.00, '2021-04-01', 'Annual Increment'),
(12, 130000.00, 145000.00, '2020-04-01', 'Annual Increment'),
(12, 145000.00, 160000.00, '2021-04-01', 'Promotion'),
(16, 70000.00, 85000.00, '2022-04-01', 'Annual Increment'),
(17, 68000.00, 82000.00, '2022-04-01', 'Annual Increment'),
(9, 95000.00, 110000.00, '2021-04-01', 'Annual Increment'),
(9, 110000.00, 130000.00, '2022-04-01', 'Promotion'),
(3, 180000.00, 200000.00, '2019-04-01', 'Annual Increment'),
(3, 200000.00, 220000.00, '2020-04-01', 'Promotion'),
(25, 95000.00, 120000.00, '2021-04-01', 'Promotion'),
(15, 140000.00, 160000.00, '2020-04-01', 'Annual Increment'),
(15, 160000.00, 170000.00, '2021-04-01', 'Annual Increment');

-- ===================== PROJECTS =====================
INSERT INTO projects (project_name, start_date, end_date, budget, status, dept_id) VALUES
('E-Commerce Platform v2', '2023-01-15', '2023-12-31', 2000000.00, 'completed', 1),
('Mobile App Development', '2023-06-01', '2024-06-30', 1500000.00, 'active', 1),
('Brand Refresh Campaign', '2023-03-01', '2023-09-30', 500000.00, 'completed', 2),
('North India Expansion', '2023-07-01', '2024-03-31', 800000.00, 'active', 3),
('Employee Wellness Program', '2023-04-01', '2023-12-31', 200000.00, 'completed', 4),
('Financial Audit 2023', '2023-10-01', '2024-01-31', 300000.00, 'completed', 5),
('Warehouse Automation', '2024-01-01', '2024-12-31', 3000000.00, 'active', 6),
('AI Chatbot', '2023-09-01', '2024-09-30', 1200000.00, 'active', 8),
('Data Migration', '2023-11-01', '2024-02-28', 400000.00, 'completed', 1),
('Customer Loyalty Program', '2024-02-01', '2024-08-31', 600000.00, 'active', 3),
('Cloud Infrastructure Upgrade', '2024-03-01', NULL, 1800000.00, 'active', 1),
('Market Research India T2', '2024-01-15', '2024-05-31', 350000.00, 'on_hold', 2),
('Legacy System Decommission', '2023-08-01', '2023-12-15', 250000.00, 'cancelled', 1);

-- ===================== EMPLOYEE PROJECTS =====================
INSERT INTO employee_projects (emp_id, project_id, role, hours_worked, assigned_date) VALUES
(1, 1, 'Project Sponsor', 50, '2023-01-15'),
(6, 1, 'Lead Developer', 800, '2023-01-20'),
(7, 1, 'Backend Developer', 750, '2023-01-20'),
(12, 1, 'Tech Architect', 400, '2023-01-15'),
(16, 1, 'Developer', 600, '2023-02-01'),
(17, 1, 'Developer', 550, '2023-02-01'),
(1, 2, 'Project Sponsor', 20, '2023-06-01'),
(12, 2, 'Tech Lead', 500, '2023-06-01'),
(18, 2, 'Developer', 400, '2023-06-15'),
(30, 2, 'Developer', 350, '2023-07-01'),
(25, 11, 'DevOps Lead', 200, '2024-03-01'),
(6, 11, 'Developer', 150, '2024-03-15'),
(2, 3, 'Project Owner', 100, '2023-03-01'),
(8, 3, 'Campaign Manager', 300, '2023-03-01'),
(19, 3, 'Content Creator', 250, '2023-03-15'),
(3, 4, 'Project Owner', 80, '2023-07-01'),
(9, 4, 'Sales Lead', 400, '2023-07-01'),
(20, 4, 'Field Executive', 500, '2023-07-15'),
(21, 4, 'Field Executive', 450, '2023-07-15'),
(15, 8, 'Research Lead', 600, '2023-09-01'),
(24, 8, 'Data Analyst', 400, '2023-09-15'),
(4, 5, 'Project Owner', 60, '2023-04-01'),
(10, 5, 'Program Manager', 200, '2023-04-01'),
(22, 5, 'Coordinator', 150, '2023-04-15'),
(25, 9, 'DevOps Lead', 300, '2023-11-01'),
(7, 9, 'Developer', 200, '2023-11-15'),
(11, 6, 'Audit Lead', 250, '2023-10-01'),
(23, 6, 'Junior Auditor', 200, '2023-10-15'),
(13, 7, 'Operations Lead', 300, '2024-01-01'),
(26, 10, 'Product Lead', 200, '2024-02-01');

-- ===================== CATEGORIES =====================
INSERT INTO categories (category_name, parent_category_id, description) VALUES
('Electronics', NULL, 'Electronic devices and accessories'),
('Clothing', NULL, 'Apparel and fashion'),
('Books', NULL, 'Physical and digital books'),
('Home & Kitchen', NULL, 'Home appliances and kitchen items'),
('Sports & Fitness', NULL, 'Sports equipment and fitness gear'),
('Smartphones', 1, 'Mobile phones and accessories'),
('Laptops', 1, 'Laptop computers'),
('Audio', 1, 'Headphones, speakers, earbuds'),
('Men''s Clothing', 2, 'Men''s apparel'),
('Women''s Clothing', 2, 'Women''s apparel'),
('Fiction', 3, 'Fiction books'),
('Non-Fiction', 3, 'Non-fiction and educational books'),
('Kitchen Appliances', 4, 'Small kitchen appliances'),
('Furniture', 4, 'Home furniture'),
('Cricket', 5, 'Cricket equipment'),
('Running', 5, 'Running shoes and gear');

-- ===================== SUPPLIERS =====================
INSERT INTO suppliers (company_name, contact_name, contact_email, phone, city, country, rating) VALUES
('TechSource India', 'Ramesh Khanna', 'ramesh@techsource.in', '9111111111', 'Shenzhen', 'China', 4.20),
('FashionHub Pvt Ltd', 'Seema Bajaj', 'seema@fashionhub.in', '9222222222', 'Mumbai', 'India', 3.80),
('BookWorld Distributors', 'Ajay Tandon', 'ajay@bookworld.in', '9333333333', 'Delhi', 'India', 4.50),
('HomeComfort Supplies', 'Nita Shah', 'nita@homecomfort.in', '9444444444', 'Ahmedabad', 'India', 3.50),
('SportsPro International', 'David Lee', 'david@sportspro.com', '9555555555', 'Singapore', 'Singapore', 4.70),
('GlobalTech Components', 'Li Wei', 'liwei@globaltech.cn', '9666666666', 'Shenzhen', 'China', 4.00),
('Desi Threads', 'Meghna Reddy', 'meghna@desithreads.in', '9777777777', 'Bangalore', 'India', 4.30),
('Kitchen Kings', 'Sunil Grover', 'sunil@kitchenkings.in', '9888888888', 'Pune', 'India', 3.90),
('FurniCraft', 'Anand Joshi', 'anand@furnicraft.in', '9999999999', 'Jodhpur', 'India', 4.10),
('RunFast Gear', 'Sarah Johnson', 'sarah@runfastgear.com', '9000000000', 'Portland', 'USA', 4.60);

-- ===================== PRODUCTS =====================
INSERT INTO products (product_name, category_id, supplier_id, unit_price, cost_price, units_in_stock, units_on_order, reorder_level, discontinued, weight_kg) VALUES
-- Smartphones
('Samsung Galaxy S24', 6, 1, 79999.00, 55000.00, 150, 50, 30, FALSE, 0.19),
('iPhone 15 Pro', 6, 1, 134900.00, 95000.00, 80, 30, 20, FALSE, 0.21),
('OnePlus 12', 6, 6, 64999.00, 42000.00, 200, 0, 40, FALSE, 0.22),
('Redmi Note 13', 6, 6, 17999.00, 11000.00, 500, 100, 100, FALSE, 0.20),
('Samsung Galaxy S23', 6, 1, 54999.00, 38000.00, 30, 0, 20, TRUE, 0.19),
-- Laptops
('MacBook Air M3', 7, 1, 114900.00, 82000.00, 60, 20, 15, FALSE, 1.24),
('Dell XPS 15', 7, 1, 145000.00, 98000.00, 40, 10, 10, FALSE, 1.86),
('Lenovo ThinkPad X1', 7, 6, 135000.00, 90000.00, 35, 15, 10, FALSE, 1.36),
('HP Pavilion 15', 7, 6, 65000.00, 42000.00, 120, 30, 25, FALSE, 1.75),
('Asus VivoBook', 7, 6, 45000.00, 28000.00, 200, 50, 40, FALSE, 1.70),
-- Audio
('Sony WH-1000XM5', 8, 1, 29990.00, 18000.00, 100, 25, 20, FALSE, 0.25),
('Apple AirPods Pro 2', 8, 1, 24900.00, 16000.00, 150, 0, 30, FALSE, 0.05),
('JBL Flip 6', 8, 6, 9999.00, 5500.00, 300, 50, 50, FALSE, 0.55),
('boAt Airdopes 141', 8, 6, 1299.00, 400.00, 1000, 200, 200, FALSE, 0.04),
-- Men's Clothing
('Levi''s 511 Slim Jeans', 9, 2, 3499.00, 1800.00, 250, 0, 50, FALSE, 0.80),
('Peter England Formal Shirt', 9, 7, 1799.00, 800.00, 400, 100, 80, FALSE, 0.30),
('Nike Dri-FIT T-Shirt', 9, 5, 2499.00, 1200.00, 300, 50, 60, FALSE, 0.25),
-- Women's Clothing
('Biba Anarkali Kurta', 10, 7, 2999.00, 1400.00, 200, 30, 40, FALSE, 0.45),
('W Cotton Palazzo', 10, 7, 1499.00, 700.00, 350, 50, 70, FALSE, 0.35),
('Puma Running Track Pants', 10, 5, 2799.00, 1300.00, 180, 40, 30, FALSE, 0.40),
-- Fiction Books
('The Guide - R.K. Narayan', 11, 3, 299.00, 120.00, 500, 0, 100, FALSE, 0.30),
('Shantaram - Gregory D Roberts', 11, 3, 599.00, 250.00, 200, 0, 50, FALSE, 0.70),
('The White Tiger - Aravind Adiga', 11, 3, 350.00, 150.00, 300, 0, 60, FALSE, 0.35),
-- Non-Fiction Books
('Atomic Habits - James Clear', 12, 3, 499.00, 200.00, 800, 100, 150, FALSE, 0.35),
('Sapiens - Yuval Noah Harari', 12, 3, 599.00, 280.00, 400, 50, 80, FALSE, 0.50),
('Zero to One - Peter Thiel', 12, 3, 399.00, 170.00, 350, 0, 70, FALSE, 0.30),
-- Kitchen Appliances
('Prestige Induction Cooktop', 13, 8, 3499.00, 2000.00, 100, 20, 20, FALSE, 2.50),
('Philips Air Fryer HD9200', 13, 4, 7999.00, 4800.00, 60, 15, 15, FALSE, 4.50),
('Bajaj Mixer Grinder', 13, 8, 2999.00, 1600.00, 150, 30, 30, FALSE, 3.20),
('Butterfly Gas Stove 3 Burner', 13, 4, 4999.00, 3000.00, 80, 0, 15, FALSE, 8.00),
-- Furniture
('Urban Ladder Study Desk', 14, 9, 12999.00, 7500.00, 30, 10, 5, FALSE, 25.00),
('Nilkamal Plastic Chair', 14, 9, 1499.00, 600.00, 500, 100, 100, FALSE, 3.50),
('Wakefit Ortho Mattress Queen', 14, 9, 8999.00, 5000.00, 40, 15, 8, FALSE, 20.00),
-- Cricket
('SG Test Cricket Bat', 15, 5, 5999.00, 3200.00, 75, 20, 15, FALSE, 1.20),
('MRF Genius Grand Edition Bat', 15, 5, 12999.00, 8000.00, 25, 5, 5, FALSE, 1.25),
('Kookaburra Cricket Ball (Pack 6)', 15, 5, 2499.00, 1200.00, 200, 0, 40, FALSE, 0.96),
-- Running
('Nike Air Zoom Pegasus 40', 16, 10, 11999.00, 6500.00, 100, 30, 20, FALSE, 0.60),
('Asics Gel-Kayano 30', 16, 10, 14999.00, 8500.00, 60, 20, 10, FALSE, 0.65),
('Garmin Forerunner 265', 16, 10, 42990.00, 28000.00, 25, 10, 5, FALSE, 0.05),
('Fitbit Charge 6', 16, 10, 14999.00, 9000.00, 80, 20, 15, FALSE, 0.04);

-- ===================== CUSTOMERS =====================
INSERT INTO customers (first_name, last_name, email, phone, city, state, country, registration_date, is_premium, credit_limit) VALUES
('Aarav', 'Sharma', 'aarav.sharma@email.com', '8001000001', 'Mumbai', 'Maharashtra', 'India', '2022-01-15', TRUE, 200000.00),
('Vivaan', 'Patel', 'vivaan.patel@email.com', '8001000002', 'Ahmedabad', 'Gujarat', 'India', '2022-02-20', FALSE, 50000.00),
('Aditya', 'Gupta', 'aditya.gupta@email.com', '8001000003', 'Delhi', 'Delhi', 'India', '2022-03-10', TRUE, 150000.00),
('Vihaan', 'Singh', 'vihaan.singh@email.com', '8001000004', 'Chandigarh', 'Punjab', 'India', '2022-04-05', FALSE, 50000.00),
('Arjun', 'Reddy', 'arjun.reddy@email.com', '8001000005', 'Hyderabad', 'Telangana', 'India', '2022-05-12', TRUE, 300000.00),
('Reyansh', 'Kumar', 'reyansh.kumar@email.com', '8001000006', 'Bangalore', 'Karnataka', 'India', '2022-06-18', FALSE, 50000.00),
('Muhammad', 'Khan', 'muhammad.khan@email.com', '8001000007', 'Lucknow', 'Uttar Pradesh', 'India', '2022-07-22', FALSE, 50000.00),
('Sai', 'Iyer', 'sai.iyer@email.com', '8001000008', 'Chennai', 'Tamil Nadu', 'India', '2022-08-30', TRUE, 100000.00),
('Arnav', 'Joshi', 'arnav.joshi@email.com', '8001000009', 'Pune', 'Maharashtra', 'India', '2022-09-14', FALSE, 50000.00),
('Dhruv', 'Nair', 'dhruv.nair@email.com', '8001000010', 'Kochi', 'Kerala', 'India', '2022-10-25', FALSE, 50000.00),
('Ishaan', 'Mehta', 'ishaan.mehta@email.com', '8001000011', 'Surat', 'Gujarat', 'India', '2022-11-05', FALSE, 75000.00),
('Anaya', 'Desai', 'anaya.desai@email.com', '8001000012', 'Mumbai', 'Maharashtra', 'India', '2022-12-01', TRUE, 250000.00),
('Saanvi', 'Bhatt', 'saanvi.bhatt@email.com', '8001000013', 'Bangalore', 'Karnataka', 'India', '2023-01-10', FALSE, 50000.00),
('Myra', 'Pandey', 'myra.pandey@email.com', '8001000014', 'Jaipur', 'Rajasthan', 'India', '2023-02-15', FALSE, 50000.00),
('Aadhya', 'Mishra', 'aadhya.mishra@email.com', '8001000015', 'Bhopal', 'Madhya Pradesh', 'India', '2023-03-20', TRUE, 175000.00),
('Diya', 'Das', 'diya.das@email.com', '8001000016', 'Kolkata', 'West Bengal', 'India', '2023-04-25', FALSE, 60000.00),
('Anika', 'Saxena', 'anika.saxena@email.com', '8001000017', 'Delhi', 'Delhi', 'India', '2023-05-30', FALSE, 50000.00),
('Kavya', 'Pillai', 'kavya.pillai@email.com', '8001000018', 'Trivandrum', 'Kerala', 'India', '2023-06-15', FALSE, 50000.00),
('Riya', 'Agarwal', 'riya.agarwal@email.com', '8001000019', 'Noida', 'Uttar Pradesh', 'India', '2023-07-20', TRUE, 120000.00),
('Neil', 'Kapoor', 'neil.kapoor@email.com', '8001000020', 'Mumbai', 'Maharashtra', 'India', '2023-08-10', FALSE, 80000.00),
('Kabir', 'Malhotra', 'kabir.malhotra@email.com', '8001000021', 'Gurgaon', 'Haryana', 'India', '2023-09-05', TRUE, 200000.00),
('Kiara', 'Verma', 'kiara.verma@email.com', '8001000022', 'Bangalore', 'Karnataka', 'India', '2023-10-12', FALSE, 50000.00),
('Zara', 'Khan', 'zara.khan@email.com', '8001000023', 'Hyderabad', 'Telangana', 'India', '2023-11-18', FALSE, 50000.00),
('Advait', 'Rao', 'advait.rao@email.com', '8001000024', 'Chennai', 'Tamil Nadu', 'India', '2023-12-01', FALSE, 50000.00),
('Rudra', 'Srinivasan', 'rudra.srinivasan@email.com', '8001000025', 'Bangalore', 'Karnataka', 'India', '2024-01-15', TRUE, 150000.00);

-- ===================== SHIPPING ADDRESSES =====================
INSERT INTO shipping_addresses (customer_id, address_line1, address_line2, city, state, postal_code, is_default) VALUES
(1, '42 Marine Drive', 'Apt 1201', 'Mumbai', 'Maharashtra', '400002', TRUE),
(1, '15 Linking Road, Bandra', NULL, 'Mumbai', 'Maharashtra', '400050', FALSE),
(3, '78 Connaught Place', 'Block B', 'Delhi', 'Delhi', '110001', TRUE),
(5, '23 Jubilee Hills', 'Road No 10', 'Hyderabad', 'Telangana', '500033', TRUE),
(5, '101 Banjara Hills', NULL, 'Hyderabad', 'Telangana', '500034', FALSE),
(8, '56 Anna Nagar', '2nd Street', 'Chennai', 'Tamil Nadu', '600040', TRUE),
(12, '89 Powai Lake Road', 'Tower C', 'Mumbai', 'Maharashtra', '400076', TRUE),
(19, 'A-45 Sector 62', NULL, 'Noida', 'Uttar Pradesh', '201301', TRUE),
(21, '12 DLF Phase 3', 'Cyber City', 'Gurgaon', 'Haryana', '122002', TRUE),
(25, '34 Koramangala 4th Block', '2nd Floor', 'Bangalore', 'Karnataka', '560034', TRUE);

-- ===================== ORDERS =====================
-- Generating diverse orders across different dates and statuses
INSERT INTO orders (customer_id, order_date, shipped_date, delivered_date, status, payment_method, shipping_cost, discount_pct, notes) VALUES
-- 2023 orders
(1, '2023-01-20 10:30:00', '2023-01-22 14:00:00', '2023-01-25 11:00:00', 'delivered', 'credit_card', 99.00, 0, NULL),
(3, '2023-02-14 09:15:00', '2023-02-16 10:00:00', '2023-02-19 15:30:00', 'delivered', 'UPI', 0, 5.00, 'Valentine gift'),
(5, '2023-03-05 16:45:00', '2023-03-07 09:00:00', '2023-03-10 12:00:00', 'delivered', 'debit_card', 49.00, 10.00, NULL),
(1, '2023-04-10 11:20:00', '2023-04-12 08:00:00', '2023-04-15 14:00:00', 'delivered', 'credit_card', 0, 0, 'Premium free shipping'),
(8, '2023-05-18 14:00:00', '2023-05-20 11:00:00', '2023-05-23 16:00:00', 'delivered', 'net_banking', 149.00, 0, NULL),
(12, '2023-06-22 08:30:00', '2023-06-24 10:00:00', '2023-06-27 09:00:00', 'delivered', 'credit_card', 0, 15.00, 'Sale discount'),
(2, '2023-07-15 17:45:00', '2023-07-17 12:00:00', '2023-07-20 10:00:00', 'delivered', 'UPI', 99.00, 0, NULL),
(4, '2023-08-25 12:00:00', '2023-08-28 09:00:00', '2023-09-01 11:00:00', 'delivered', 'COD', 199.00, 0, NULL),
(9, '2023-09-10 10:00:00', '2023-09-12 14:00:00', '2023-09-15 10:00:00', 'delivered', 'UPI', 49.00, 5.00, NULL),
(6, '2023-10-15 15:30:00', '2023-10-17 11:00:00', '2023-10-20 14:00:00', 'delivered', 'debit_card', 0, 0, NULL),
(10, '2023-11-24 09:00:00', '2023-11-26 08:00:00', '2023-11-29 12:00:00', 'delivered', 'credit_card', 99.00, 20.00, 'Black Friday sale'),
(15, '2023-12-20 18:00:00', '2023-12-22 10:00:00', '2023-12-26 11:00:00', 'delivered', 'UPI', 149.00, 10.00, 'Christmas order'),
-- 2024 orders
(1, '2024-01-05 10:00:00', '2024-01-07 09:00:00', '2024-01-10 14:00:00', 'delivered', 'credit_card', 0, 0, NULL),
(3, '2024-01-15 14:30:00', '2024-01-17 10:00:00', '2024-01-20 11:00:00', 'delivered', 'UPI', 49.00, 0, NULL),
(5, '2024-02-10 11:00:00', '2024-02-12 08:00:00', '2024-02-15 16:00:00', 'delivered', 'credit_card', 0, 5.00, NULL),
(12, '2024-02-14 09:00:00', '2024-02-16 10:00:00', '2024-02-19 12:00:00', 'delivered', 'debit_card', 99.00, 0, 'Valentine special'),
(19, '2024-03-01 16:00:00', '2024-03-03 11:00:00', '2024-03-06 10:00:00', 'delivered', 'UPI', 0, 10.00, NULL),
(21, '2024-03-15 08:45:00', '2024-03-17 09:00:00', '2024-03-20 15:00:00', 'delivered', 'credit_card', 0, 0, NULL),
(7, '2024-04-05 12:30:00', '2024-04-07 10:00:00', '2024-04-10 11:00:00', 'delivered', 'net_banking', 99.00, 0, NULL),
(13, '2024-04-20 15:00:00', '2024-04-22 14:00:00', '2024-04-25 10:00:00', 'delivered', 'UPI', 49.00, 5.00, NULL),
(16, '2024-05-10 09:30:00', '2024-05-12 08:00:00', '2024-05-15 14:00:00', 'delivered', 'debit_card', 99.00, 0, NULL),
(20, '2024-05-25 17:00:00', '2024-05-27 10:00:00', '2024-05-30 11:00:00', 'delivered', 'credit_card', 0, 0, NULL),
(25, '2024-06-01 10:15:00', '2024-06-03 09:00:00', '2024-06-06 16:00:00', 'delivered', 'UPI', 0, 15.00, 'Premium member discount'),
(11, '2024-06-15 14:00:00', '2024-06-17 10:00:00', '2024-06-20 12:00:00', 'delivered', 'net_banking', 149.00, 0, NULL),
(14, '2024-07-04 11:30:00', '2024-07-06 08:00:00', '2024-07-09 10:00:00', 'delivered', 'COD', 199.00, 0, NULL),
(22, '2024-07-20 16:00:00', '2024-07-22 11:00:00', '2024-07-25 14:00:00', 'delivered', 'UPI', 49.00, 0, NULL),
(17, '2024-08-05 08:00:00', '2024-08-07 09:00:00', '2024-08-10 11:00:00', 'delivered', 'debit_card', 99.00, 5.00, NULL),
(23, '2024-08-18 13:00:00', '2024-08-20 10:00:00', '2024-08-23 15:00:00', 'delivered', 'credit_card', 0, 0, NULL),
(24, '2024-09-10 10:00:00', '2024-09-12 14:00:00', NULL, 'shipped', 'UPI', 99.00, 0, NULL),
(18, '2024-09-20 15:30:00', NULL, NULL, 'processing', 'net_banking', 149.00, 10.00, NULL),
(5, '2024-10-01 09:00:00', '2024-10-03 08:00:00', '2024-10-06 12:00:00', 'delivered', 'credit_card', 0, 0, NULL),
(1, '2024-10-15 14:00:00', '2024-10-17 10:00:00', NULL, 'shipped', 'credit_card', 0, 5.00, NULL),
(21, '2024-10-25 11:00:00', NULL, NULL, 'processing', 'UPI', 99.00, 0, NULL),
(3, '2024-11-01 10:30:00', NULL, NULL, 'pending', 'credit_card', 49.00, 0, NULL),
(12, '2024-11-10 16:00:00', NULL, NULL, 'pending', 'UPI', 0, 20.00, 'Diwali sale'),
(9, '2024-11-15 08:00:00', NULL, NULL, 'cancelled', 'COD', 199.00, 0, 'Customer requested cancellation'),
(6, '2024-11-20 12:00:00', NULL, NULL, 'pending', 'debit_card', 99.00, 0, NULL),
(15, '2024-11-25 14:30:00', NULL, NULL, 'pending', 'credit_card', 0, 10.00, NULL),
(25, '2024-12-01 09:00:00', '2024-12-03 10:00:00', NULL, 'shipped', 'UPI', 0, 0, NULL),
(5, '2024-12-10 11:00:00', NULL, NULL, 'pending', 'credit_card', 0, 15.00, 'Year-end sale'),
-- Returned orders
(2, '2024-06-10 10:00:00', '2024-06-12 09:00:00', '2024-06-15 11:00:00', 'returned', 'UPI', 99.00, 0, 'Wrong size delivered');

-- ===================== ORDER ITEMS =====================
INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount) VALUES
-- Order 1: Customer bought phone + case
(1, 1, 1, 79999.00, 0),       -- Samsung Galaxy S24
(1, 14, 2, 1299.00, 0),       -- boAt Airdopes x2
-- Order 2: Valentine gift
(2, 18, 1, 2999.00, 0),       -- Biba Kurta
(2, 24, 1, 499.00, 0),        -- Atomic Habits
-- Order 3: Electronics haul
(3, 2, 1, 134900.00, 10.00),  -- iPhone 15 Pro with 10% discount
(3, 11, 1, 29990.00, 10.00),  -- Sony headphones
-- Order 4: Books
(4, 21, 1, 299.00, 0),        -- The Guide
(4, 22, 1, 599.00, 0),        -- Shantaram
(4, 24, 1, 499.00, 0),        -- Atomic Habits
(4, 25, 1, 599.00, 0),        -- Sapiens
-- Order 5: Kitchen
(5, 27, 1, 3499.00, 0),       -- Prestige Induction
(5, 29, 1, 2999.00, 0),       -- Bajaj Mixer
-- Order 6: Everything sale
(6, 6, 1, 114900.00, 15.00),  -- MacBook Air
(6, 12, 1, 24900.00, 15.00),  -- AirPods
(6, 17, 2, 2499.00, 15.00),   -- Nike T-Shirt x2
-- Order 7: Clothing
(7, 15, 2, 3499.00, 0),       -- Levi's Jeans x2
(7, 16, 3, 1799.00, 0),       -- Peter England Shirt x3
-- Order 8: Sports
(8, 34, 1, 5999.00, 0),       -- SG Cricket Bat
(8, 36, 2, 2499.00, 0),       -- Cricket Ball x2
-- Order 9: Home
(9, 31, 1, 12999.00, 5.00),   -- Study Desk
(9, 32, 4, 1499.00, 5.00),    -- Chairs x4
-- Order 10: Running gear
(10, 37, 1, 11999.00, 0),     -- Nike Pegasus
(10, 39, 1, 42990.00, 0),     -- Garmin Watch
-- Order 11: Big Black Friday
(11, 7, 1, 145000.00, 20.00), -- Dell XPS
(11, 11, 1, 29990.00, 20.00), -- Sony WH-1000XM5
(11, 39, 1, 42990.00, 20.00), -- Garmin
-- Order 12: Christmas
(12, 28, 1, 7999.00, 10.00),  -- Air Fryer
(12, 33, 1, 8999.00, 10.00),  -- Mattress
-- Order 13
(13, 3, 1, 64999.00, 0),      -- OnePlus 12
(13, 14, 3, 1299.00, 0),      -- boAt Airdopes x3
-- Order 14
(14, 8, 1, 135000.00, 0),     -- ThinkPad
-- Order 15
(15, 35, 1, 12999.00, 5.00),  -- MRF Bat
(15, 37, 1, 11999.00, 5.00),  -- Nike Pegasus
(15, 34, 2, 5999.00, 5.00),   -- SG Bat x2
-- Order 16
(16, 19, 2, 1499.00, 0),      -- Palazzo x2
(16, 20, 1, 2799.00, 0),      -- Puma Track Pants
-- Order 17
(17, 4, 1, 17999.00, 10.00),  -- Redmi Note 13
(17, 14, 1, 1299.00, 0),      -- boAt Airdopes
-- Order 18
(18, 7, 1, 145000.00, 0),     -- Dell XPS
(18, 12, 1, 24900.00, 0),     -- AirPods
-- Order 19
(19, 30, 1, 4999.00, 0),      -- Gas Stove
(19, 27, 1, 3499.00, 0),      -- Induction
-- Order 20
(20, 26, 2, 399.00, 5.00),    -- Zero to One x2
(20, 23, 1, 350.00, 0),       -- White Tiger
-- Order 21
(21, 10, 1, 45000.00, 0),     -- Asus VivoBook
-- Order 22
(22, 9, 1, 65000.00, 0),      -- HP Pavilion
-- Order 23
(23, 38, 1, 14999.00, 15.00), -- Asics Kayano
(23, 40, 1, 14999.00, 15.00), -- Fitbit
-- Order 24
(24, 13, 2, 9999.00, 0),      -- JBL Flip x2
(24, 14, 5, 1299.00, 0),      -- boAt Airdopes x5
-- Order 25
(25, 33, 1, 8999.00, 0),      -- Mattress
(25, 31, 1, 12999.00, 0),     -- Study Desk
(25, 32, 6, 1499.00, 0),      -- Chairs x6
-- Order 26
(26, 37, 1, 11999.00, 0),     -- Nike Pegasus
(26, 17, 1, 2499.00, 0),      -- Nike T-Shirt
-- Order 27
(27, 15, 1, 3499.00, 5.00),   -- Levi's Jeans
(27, 16, 2, 1799.00, 0),      -- Peter England x2
-- Order 28
(28, 2, 1, 134900.00, 0),     -- iPhone 15 Pro
-- Order 29
(29, 6, 1, 114900.00, 0),     -- MacBook Air M3
-- Order 30
(30, 38, 1, 14999.00, 0),     -- Asics Kayano
-- Order 31
(31, 1, 1, 79999.00, 0),      -- Samsung S24
(31, 11, 1, 29990.00, 5.00),  -- Sony headphones
-- Order 32
(32, 28, 2, 7999.00, 0),      -- Air Fryer x2
(32, 29, 1, 2999.00, 0),      -- Bajaj Mixer
-- Order 33
(33, 24, 3, 499.00, 0),       -- Atomic Habits x3
(33, 25, 2, 599.00, 0),       -- Sapiens x2
-- Order 34
(34, 3, 2, 64999.00, 20.00),  -- OnePlus 12 x2
(34, 14, 10, 1299.00, 20.00), -- boAt Airdopes x10
-- Order 35: Cancelled
(35, 7, 1, 145000.00, 0),     -- Dell XPS
-- Order 36
(36, 4, 2, 17999.00, 0),      -- Redmi Note 13 x2
(36, 13, 1, 9999.00, 0),      -- JBL Flip
-- Order 37
(37, 35, 1, 12999.00, 10.00), -- MRF Bat
(37, 38, 1, 14999.00, 10.00), -- Asics
-- Order 38
(38, 1, 1, 79999.00, 0),      -- Samsung S24
-- Order 39
(39, 2, 1, 134900.00, 15.00), -- iPhone 15 Pro
(39, 6, 1, 114900.00, 15.00), -- MacBook Air
-- Order 40: returned
(40, 17, 3, 2499.00, 0),      -- Nike T-Shirt x3
(40, 15, 1, 3499.00, 0);      -- Levi's Jeans

-- ===================== REVIEWS =====================
INSERT INTO reviews (product_id, customer_id, rating, review_text, review_date, is_verified_purchase) VALUES
(1, 1, 5, 'Amazing phone! Camera quality is top notch. Battery lasts all day.', '2023-01-28', TRUE),
(2, 5, 5, 'Best iPhone ever. The titanium build feels premium. A15 Bionic is blazing fast.', '2023-03-15', TRUE),
(2, 3, 4, 'Great phone but too expensive. Face ID works perfectly though.', '2024-01-25', TRUE),
(3, 1, 4, 'Good value for money. OxygenOS is clean and fast.', '2024-01-15', TRUE),
(4, 19, 5, 'Best budget phone. AMOLED display at this price is incredible.', '2024-03-10', TRUE),
(6, 12, 5, 'M3 chip is revolutionary. 18 hour battery life. Fanless design is silky silent.', '2023-07-02', TRUE),
(6, 21, 5, 'Perfect for coding and everyday use. Insanely fast.', '2024-03-25', TRUE),
(7, 10, 4, 'Beautiful display but runs a bit hot under load. Keyboard is excellent.', '2023-12-05', TRUE),
(9, 22, 4, 'Solid laptop for the price. Good for students and light work.', '2024-07-28', TRUE),
(11, 5, 5, 'Industry-leading noise cancellation. Sound quality is phenomenal.', '2023-03-12', TRUE),
(11, 10, 4, 'Great headphones but the price is steep. ANC is best in class.', '2023-12-02', TRUE),
(12, 12, 4, 'Good ANC for the size. Seamless with Apple ecosystem.', '2023-07-01', TRUE),
(13, 11, 5, 'Awesome portable speaker! Bass is punchy. Waterproof is a bonus.', '2024-06-22', TRUE),
(14, 1, 3, 'Decent for the price. Sound is okay, not great. Battery life is good.', '2023-01-28', TRUE),
(14, 19, 4, 'Best earbuds under 1500. Build quality could be better.', '2024-03-08', TRUE),
(14, 6, 3, 'Average sound quality but can''t complain at this price point.', '2024-12-01', FALSE),
(15, 2, 5, 'Classic Levi''s quality. Perfect fit and very comfortable.', '2023-07-25', TRUE),
(16, 2, 4, 'Good formal shirt. Fabric is comfortable. Collar stays crisp.', '2023-07-25', TRUE),
(17, 6, 5, 'Dri-FIT technology works great. Keeps you cool during workouts.', '2023-10-22', TRUE),
(17, 22, 4, 'Nice material and fit. Slightly overpriced for a t-shirt.', '2024-07-27', TRUE),
(18, 3, 5, 'Beautiful design. Fabric quality is excellent. True to size.', '2023-02-22', TRUE),
(24, 1, 5, 'Game-changing book. The 1% improvement concept is powerful. Must read!', '2023-04-20', TRUE),
(24, 3, 5, 'Life-changing read. Simple yet effective strategies.', '2023-02-22', TRUE),
(24, 13, 4, 'Good book with practical advice. Could be shorter though.', '2024-04-28', TRUE),
(25, 1, 5, 'Mind-blowing perspective on human history. Dense but fascinating.', '2023-04-20', TRUE),
(27, 8, 4, 'Good induction cooktop. Heats up fast. Timer feature is useful.', '2023-05-26', TRUE),
(28, 12, 4, 'Air fryer changed my cooking. Less oil, same taste. A bit noisy.', '2024-12-22', FALSE),
(31, 9, 4, 'Sturdy desk, good for WFH setup. Assembly was a bit tricky.', '2023-09-18', TRUE),
(33, 25, 5, 'Best mattress I''ve ever slept on. Back pain vanished in a week.', '2023-10-05', FALSE),
(34, 4, 5, 'Premium cricket bat. Perfect balance and sweet spot. Worth every rupee.', '2023-09-05', TRUE),
(37, 6, 5, 'Most comfortable running shoe ever. Zoom Air cushioning is perfect.', '2023-10-25', TRUE),
(37, 22, 4, 'Good running shoe. Slightly heavy for racing but great for training.', '2024-07-28', TRUE),
(38, 15, 5, 'Best stability shoe on the market. Perfect for long distance.', '2024-12-01', FALSE),
(39, 6, 5, 'Amazing GPS accuracy. AMOLED display is gorgeous. Battery lasts 2 weeks.', '2023-10-24', TRUE),
(39, 23, 4, 'Great fitness tracker for runners. UI could be more intuitive.', '2024-08-25', TRUE),
(40, 15, 4, 'Decent fitness tracker. Heart rate monitoring is accurate.', '2024-12-02', FALSE),
(9, 21, 3, 'Laptop is okay. Fan noise is annoying. Screen could be brighter.', '2024-03-22', TRUE),
(29, 8, 5, 'Great mixer grinder. Handles tough grinding with ease.', '2023-05-26', TRUE),
(10, 21, 4, 'Good budget laptop for basic tasks. Build quality is plasticky.', '2024-07-20', FALSE);

-- ===================== INVENTORY LOG =====================
INSERT INTO inventory (product_id, change_qty, change_type, change_date, notes) VALUES
-- Samsung Galaxy S24
(1, 200, 'restock', '2023-01-01', 'Initial stock'),
(1, -50, 'sale', '2023-06-30', 'H1 sales'),
(1, 100, 'restock', '2023-07-15', 'Mid-year restock'),
(1, -80, 'sale', '2023-12-31', 'H2 sales'),
(1, -5, 'damaged', '2024-01-10', 'Warehouse handling damage'),
(1, 50, 'restock', '2024-03-01', 'Q1 restock'),
(1, -65, 'sale', '2024-06-30', 'H1 2024 sales'),
-- iPhone 15 Pro
(2, 100, 'restock', '2023-01-15', 'Initial stock'),
(2, -40, 'sale', '2023-06-30', 'H1 sales'),
(2, 50, 'restock', '2023-09-01', 'Launch restock'),
(2, -30, 'sale', '2024-06-30', 'Sales'),
-- OnePlus 12
(3, 250, 'restock', '2023-03-01', 'Initial stock'),
(3, -80, 'sale', '2023-12-31', 'Annual sales'),
(3, 100, 'restock', '2024-01-15', 'Restock'),
(3, -70, 'sale', '2024-09-30', 'Sales'),
-- boAt Airdopes (high volume)
(14, 1500, 'restock', '2023-01-01', 'Bulk initial stock'),
(14, -500, 'sale', '2023-06-30', 'H1 sales'),
(14, 500, 'restock', '2023-07-01', 'Restock'),
(14, -600, 'sale', '2023-12-31', 'H2 heavy season'),
(14, 300, 'restock', '2024-01-15', 'Q1 restock'),
(14, -200, 'sale', '2024-06-30', 'H1 2024'),
(14, 3, 'return', '2024-02-15', 'Customer returns'),
-- Atomic Habits
(24, 1000, 'restock', '2022-06-01', 'Initial stock'),
(24, -300, 'sale', '2023-06-30', 'H1 sales'),
(24, 200, 'restock', '2023-07-01', 'Restock'),
(24, -250, 'sale', '2023-12-31', 'H2 sales'),
(24, 300, 'restock', '2024-01-15', 'Annual restock'),
(24, -150, 'sale', '2024-09-30', 'Sales'),
-- Damaged/returns examples
(7, 50, 'restock', '2023-06-01', 'Initial stock'),
(7, -2, 'damaged', '2023-08-15', 'Screen damage in transit'),
(7, 3, 'return', '2024-01-20', 'Customer returns'),
(37, 150, 'restock', '2023-01-01', 'Initial stock'),
(37, -50, 'sale', '2023-12-31', 'Annual sales'),
(37, 30, 'restock', '2024-03-01', 'Restock'),
(37, -30, 'sale', '2024-09-30', 'Sales'),
-- Adjustments
(32, 600, 'restock', '2023-01-01', 'Initial stock'),
(32, -15, 'adjustment', '2023-06-15', 'Inventory audit correction'),
(32, -85, 'sale', '2023-12-31', 'Annual sales');

SELECT 'Dummy data inserted successfully!' AS status;
