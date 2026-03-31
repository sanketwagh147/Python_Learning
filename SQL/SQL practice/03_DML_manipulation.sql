-- =============================================================================
-- DML (Data Manipulation Language) Practice Problems
-- Database: postgresql://sanket@localhost:5432/local_db
-- 
-- INSERT, UPDATE, DELETE operations with real-world scenarios.
-- ALWAYS test with SELECT first before running UPDATE/DELETE!
-- Difficulty: 🟢 Easy  🟡 Medium  🔴 Hard
-- =============================================================================


-- =============================================================================
-- SECTION 1: INSERT Operations
-- =============================================================================

-- Q1.1 🟢 Easy
-- Insert a new department called 'Data Science' located in 'Bangalore' 
-- with a budget of 3500000.
-- Then insert 2 employees into this department.
-- HINT: INSERT INTO ... VALUES. Use currval('departments_dept_id_seq') or
-- RETURNING dept_id to capture the new ID for foreign key reference.


-- Q1.2 🟡 Medium
-- Insert a new order for customer 'Aarav Sharma' (customer_id = 1):
-- - 2x 'Atomic Habits' 
-- - 1x 'Samsung Galaxy S24'
-- - 1x 'Sony WH-1000XM5'
-- Apply a 5% discount on the Sony headphones only.
-- Payment via 'credit_card', shipping cost 0 (premium member).
-- 
-- HINT: INSERT into orders first, capture order_id with RETURNING,
-- then INSERT into order_items. Use subqueries to look up product_ids
-- and current unit_prices from the products table rather than hardcoding.
--
-- Thought: INSERT INTO order_items (order_id, product_id, quantity, unit_price, discount)
-- SELECT <new_order_id>, product_id, <qty>, unit_price, <disc>
-- FROM products WHERE product_name = '...';


-- Q1.3 🔴 Hard
-- Bulk insert: Create a "flash sale" - insert 100 orders for random 
-- customers buying random products. Use generate_series and random().
--
-- HINT: This tests INSERT ... SELECT with data generation.
-- Think about:
-- 1. Generate order rows: INSERT INTO orders SELECT ... FROM generate_series(1, 100)
-- 2. Random customer: (random() * 24 + 1)::int 
-- 3. Random products: Use a separate insert for order_items
-- 4. Be careful with valid foreign key references.
--
-- Approach: 
-- Step 1: Insert orders with random customers
-- Step 2: For each new order, insert 1-3 random order items
-- Key insight: generate_series + random() + FLOOR for integer conversion.
-- Use RETURNING to capture generated order_ids.


-- Q1.4 🟡 Medium - INSERT with conflict handling
-- Insert or update: Try to insert a review for product_id=1, customer_id=1.
-- If the review already exists, update the rating and review text instead.
-- 
-- HINT: INSERT ... ON CONFLICT (product_id, customer_id) DO UPDATE SET ...
-- This is PostgreSQL's UPSERT pattern. Very common in real applications.
-- Think about: What column(s) define the conflict? Check the UNIQUE constraint.


-- =============================================================================
-- SECTION 2: UPDATE Operations
-- =============================================================================

-- Q2.1 🟢 Easy
-- Give a 10% salary raise to all employees in the Engineering department 
-- who were hired before 2021 and are active.
-- HINT: UPDATE with subquery or JOIN for department filtering.
-- Always write a SELECT first to verify which rows will be affected!


-- Q2.2 🟡 Medium
-- Update the order status: 
-- - Mark all 'pending' orders older than 30 days as 'cancelled'
-- - For the cancelled orders, also update the notes to include 
--   'Auto-cancelled: exceeded 30 day pending limit'
-- - Log this in a hypothetical audit by appending to notes
--
-- HINT: UPDATE orders SET status = 'cancelled', 
--   notes = COALESCE(notes || ' | ', '') || 'Auto-cancelled...'
-- WHERE status = 'pending' AND order_date < CURRENT_TIMESTAMP - INTERVAL '30 days'
-- 
-- Thought: What if you want to know which orders were cancelled? 
-- Use RETURNING * to see the affected rows.


-- Q2.3 🟡 Medium
-- Update product stock levels based on recent orders:
-- For all 'delivered' orders, reduce units_in_stock by the ordered quantity.
-- But NEVER let stock go below 0.
-- 
-- HINT: UPDATE with FROM clause (PostgreSQL extension):
-- UPDATE products SET units_in_stock = GREATEST(units_in_stock - sold_qty, 0)
-- FROM (SELECT product_id, SUM(quantity) as sold_qty 
--       FROM order_items oi JOIN orders o ON ... WHERE status = 'delivered'
--       GROUP BY product_id) AS sales
-- WHERE products.product_id = sales.product_id;
--
-- Key: GREATEST(value, 0) prevents negative stock.


-- Q2.4 🔴 Hard
-- Implement a "salary normalization": Ensure no employee earns less than 
-- 80% of the average salary for their job_title. If they do, raise them to 80%.
-- Also log every change into salary_history with reason 'Salary Normalization'.
--
-- HINT: This requires:
-- 1. CTE to calculate avg salary per job_title
-- 2. Identify employees below the 80% threshold
-- 3. UPDATE those employees
-- 4. INSERT into salary_history for each affected employee
--
-- Approach: Use a CTE + UPDATE ... FROM.
-- For the history insert: INSERT INTO salary_history SELECT ... FROM employees 
-- WHERE salary < threshold (run BEFORE the update to capture old_salary).
-- Then UPDATE. This requires two statements in a transaction.
--
-- Key concept: Transaction ordering matters. What if you UPDATE first?
-- You'd lose the original salary for the history log.


-- Q2.5 🔴 Hard
-- Implement a tiered commission update:
-- Employees in Sales with total order revenue > 500K get commission_pct = 0.15
-- Revenue 200K-500K: commission_pct = 0.10
-- Revenue 100K-200K: commission_pct = 0.08
-- Revenue < 100K: commission_pct = 0.05
--
-- But: don't overwrite commission if it's already higher than the calculated tier.
--
-- HINT: UPDATE employees SET commission_pct = GREATEST(commission_pct, new_commission)
-- FROM (subquery computing revenue per salesperson) ...
--
-- Thought process: Which table links employees to orders? There's no direct link.
-- You need to think about who "owns" the order - is it the customer or an employee?
-- In this schema, orders belong to customers. So you'd need a business rule:
-- Option A: Credit orders to the Sales dept employees proportionally.
-- Option B: Simply recalculate based on total Sales dept performance.
-- This tests your ability to identify schema limitations and handle them.


-- =============================================================================
-- SECTION 3: DELETE Operations
-- =============================================================================

-- Q3.1 🟢 Easy
-- Delete all reviews that are not verified purchases and have a rating <= 2.
-- First, write a SELECT to preview which reviews will be deleted.
-- HINT: DELETE FROM reviews WHERE is_verified_purchase = FALSE AND rating <= 2;
-- ALWAYS preview with SELECT first!


-- Q3.2 🟡 Medium
-- Delete cancelled orders and their order items.
-- But FIRST, archive them: Insert into a temporary archive table before deleting.
-- 
-- HINT: 
-- Step 1: CREATE TEMP TABLE order_archive AS SELECT * FROM orders WHERE status = 'cancelled';
-- Step 2: CREATE TEMP TABLE order_items_archive AS SELECT oi.* FROM order_items oi 
--         JOIN orders o ON ... WHERE o.status = 'cancelled';
-- Step 3: DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE status = 'cancelled');
-- Step 4: DELETE FROM orders WHERE status = 'cancelled';
--
-- Thought: Order matters because of FK constraints. Delete child rows first.
-- Or use ON DELETE CASCADE (DDL change).


-- Q3.3 🔴 Hard
-- Clean up stale data: Delete customers who:
-- 1. Registered more than 2 years ago
-- 2. Have NEVER placed an order
-- 3. Are not premium members
-- But there are FK constraints (shipping_addresses reference customers).
-- Handle cascade properly.
--
-- HINT: Use NOT EXISTS for "never placed an order".
-- You need to delete from shipping_addresses first, then customers.
-- Or handle with a single DELETE using CTEs (PostgreSQL supports this):
--
-- WITH stale_customers AS (
--   SELECT customer_id FROM customers 
--   WHERE registration_date < CURRENT_DATE - INTERVAL '2 years'
--   AND NOT EXISTS (SELECT 1 FROM orders WHERE customer_id = customers.customer_id)
--   AND is_premium = FALSE
-- ),
-- deleted_addresses AS (
--   DELETE FROM shipping_addresses WHERE customer_id IN (SELECT customer_id FROM stale_customers)
--   RETURNING *
-- )
-- DELETE FROM customers WHERE customer_id IN (SELECT customer_id FROM stale_customers);
--
-- This uses writable CTEs (data-modifying CTEs), a powerful PostgreSQL feature.


-- Q3.4 🔴 Hard
-- Implement a "soft delete" pattern: Instead of actually deleting inactive employees,
-- add a 'deleted_at' column (if it doesn't exist) and set it to CURRENT_TIMESTAMP.
-- 
-- Then, write queries that behave as if deleted employees don't exist 
-- (filter WHERE deleted_at IS NULL).
-- Show: How to "undelete" (set deleted_at back to NULL).
--
-- HINT: This is a two-part problem:
-- Part 1: ALTER TABLE to add the column (DDL)
-- Part 2: UPDATE to "soft delete" (DML)
-- Part 3: Create a VIEW that filters out soft-deleted rows (DDL)
--
-- Discuss: Why is soft delete preferred in production systems?
-- Think about: audit trails, data recovery, referential integrity.


-- =============================================================================
-- SECTION 4: MERGE / UPSERT Patterns
-- =============================================================================

-- Q4.1 🟡 Medium
-- You receive a daily inventory update CSV-like data. For each product:
-- If the product exists: update units_in_stock
-- If the product doesn't exist: insert it
-- Simulate with a VALUES clause.
--
-- HINT: INSERT INTO products (...) VALUES (...)
-- ON CONFLICT (product_name) DO UPDATE SET units_in_stock = EXCLUDED.units_in_stock;
-- Note: you'd need a unique constraint on product_name for this to work.
-- Think about: What if the conflict column isn't unique? 
-- What if you want to merge on multiple columns?


-- Q4.2 🔴 Hard
-- Implement a "slowly changing dimension" Type 2 update for salary history:
-- When an employee's salary changes, don't overwrite - keep history.
-- The salary_history table already exists. Write a function/procedure or 
-- a series of SQL statements that:
-- 1. Checks if new salary differs from current
-- 2. Inserts into salary_history with old and new values
-- 3. Updates the employee's current salary
-- 4. All within a single transaction
--
-- HINT: 
-- BEGIN;
-- INSERT INTO salary_history (emp_id, old_salary, new_salary, change_date, change_reason)
-- SELECT emp_id, salary, <new_salary>, CURRENT_DATE, 'Manual Update'
-- FROM employees WHERE emp_id = <id> AND salary != <new_salary>;
-- 
-- UPDATE employees SET salary = <new_salary> WHERE emp_id = <id>;
-- COMMIT;
--
-- The INSERT only fires if the salary actually changed (WHERE salary != new_salary).
-- Discuss: Why is the transaction important? What happens if the server 
-- crashes between INSERT and UPDATE without a transaction?


-- =============================================================================
-- SECTION 5: Transactions & Concurrency Concepts
-- =============================================================================

-- Q5.1 🟡 Medium
-- Write a transaction that transfers budget between departments:
-- Move 500000 from Engineering to a new 'AI Research' department.
-- Ensure: total budget doesn't change, both operations succeed or both fail.
--
-- HINT: 
-- BEGIN;
-- SAVEPOINT before_transfer;
-- UPDATE departments SET budget = budget - 500000 WHERE dept_name = 'Engineering';
-- -- Check if Engineering had enough budget
-- -- If not: ROLLBACK TO before_transfer;
-- INSERT INTO departments (dept_name, location, budget) VALUES ('AI Research', 'Bangalore', 500000);
-- COMMIT;
--
-- Discuss: What isolation level is needed? What if two sessions 
-- try to deduct from Engineering simultaneously?


-- Q5.2 🔴 Hard
-- Simulate an order placement transaction that:
-- 1. Checks product stock availability
-- 2. Reduces stock (with row-level lock)
-- 3. Creates the order  
-- 4. Creates order items
-- 5. Logs inventory changes
-- If any product is out of stock, roll back the entire order.
--
-- HINT: Use SELECT ... FOR UPDATE to lock product rows.
-- This prevents race conditions where two orders deplete stock simultaneously.
--
-- BEGIN;
-- SELECT product_id, units_in_stock FROM products 
-- WHERE product_id IN (1, 11, 24) FOR UPDATE;
-- -- Check if all have sufficient stock
-- -- If any insufficient: ROLLBACK; RAISE NOTICE 'insufficient stock';
-- UPDATE products SET units_in_stock = units_in_stock - <qty> WHERE product_id = <id>;
-- INSERT INTO orders ... RETURNING order_id;
-- INSERT INTO order_items ...;
-- INSERT INTO inventory (product_id, change_qty, change_type) VALUES ...;
-- COMMIT;
--
-- Discuss: What's the difference between FOR UPDATE, FOR SHARE, 
-- FOR NO KEY UPDATE? When would you use each?
