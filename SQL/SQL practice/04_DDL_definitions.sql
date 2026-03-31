-- =============================================================================
-- DDL (Data Definition Language) Practice Problems
-- Database: postgresql://sanket@localhost:5432/local_db
-- 
-- ~10% focus: Table creation, alteration, constraints, indexes, views.
-- Difficulty: 🟢 Easy  🟡 Medium  🔴 Hard
-- =============================================================================


-- =============================================================================
-- SECTION 1: CREATE TABLE & Constraints
-- =============================================================================

-- Q1.1 🟢 Easy
-- Create a table 'coupons' with the following:
-- - coupon_id (auto-increment PK)
-- - coupon_code (unique, not null, uppercase enforced via CHECK)
-- - discount_type ('percentage' or 'fixed' - use CHECK)
-- - discount_value (positive number)
-- - min_order_value (default 0)
-- - max_uses (integer, default null = unlimited)
-- - times_used (default 0, must be <= max_uses when max_uses is not null)
-- - valid_from, valid_until (dates, valid_until must be after valid_from)
-- - is_active (boolean, default true)
-- 
-- HINT: CHECK (valid_until > valid_from)
-- CHECK (coupon_code = UPPER(coupon_code)) enforces uppercase.
-- The max_uses constraint is tricky: CHECK(max_uses IS NULL OR times_used <= max_uses)


-- Q1.2 🟡 Medium
-- Create an audit_log table that tracks ALL changes to the orders table:
-- - log_id, table_name, operation (INSERT/UPDATE/DELETE), 
-- - old_data (JSONB), new_data (JSONB)
-- - changed_by (defaults to current_user), changed_at (defaults to now())
-- 
-- Then create a trigger function and trigger to auto-populate this table.
-- 
-- HINT: 
-- CREATE OR REPLACE FUNCTION log_order_changes() RETURNS TRIGGER AS $$
-- BEGIN
--   IF TG_OP = 'DELETE' THEN
--     INSERT INTO audit_log(table_name, operation, old_data)
--     VALUES ('orders', 'DELETE', row_to_json(OLD)::jsonb);
--   ELSIF TG_OP = 'UPDATE' THEN
--     INSERT INTO audit_log(table_name, operation, old_data, new_data)
--     VALUES ('orders', 'UPDATE', row_to_json(OLD)::jsonb, row_to_json(NEW)::jsonb);
--   ELSIF TG_OP = 'INSERT' THEN
--     INSERT INTO audit_log(table_name, operation, new_data)
--     VALUES ('orders', 'INSERT', row_to_json(NEW)::jsonb);
--   END IF;
--   RETURN NEW;
-- END;
-- $$ LANGUAGE plpgsql;


-- Q1.3 🔴 Hard
-- Create a partitioned orders_archive table partitioned by RANGE on order_date.
-- Create partitions for each quarter of 2023 and 2024.
-- Insert some data and verify partition pruning works.
--
-- HINT: 
-- CREATE TABLE orders_archive (LIKE orders INCLUDING ALL) PARTITION BY RANGE (order_date);
-- CREATE TABLE orders_archive_2023_q1 PARTITION OF orders_archive
--   FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
-- 
-- Discuss: When is partitioning beneficial? What are the trade-offs?
-- Think about: Partition pruning in EXPLAIN, maintenance overhead.


-- =============================================================================
-- SECTION 2: ALTER TABLE
-- =============================================================================

-- Q2.1 🟢 Easy
-- Add a 'loyalty_points' column to the customers table (integer, default 0).
-- Add a 'last_login' column (timestamp, nullable).
-- HINT: ALTER TABLE customers ADD COLUMN loyalty_points INT DEFAULT 0;


-- Q2.2 🟡 Medium
-- The products table needs a full-text search capability on product_name.
-- Add a tsvector column, populate it, create a GIN index, and create a 
-- trigger to keep it updated on INSERT/UPDATE.
--
-- HINT:
-- ALTER TABLE products ADD COLUMN search_vector tsvector;
-- UPDATE products SET search_vector = to_tsvector('english', product_name);
-- CREATE INDEX idx_products_search ON products USING GIN(search_vector);
-- 
-- Create trigger to auto-update:
-- CREATE TRIGGER products_search_update BEFORE INSERT OR UPDATE ON products
-- FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(search_vector, 'pg_catalog.english', product_name);


-- Q2.3 🔴 Hard
-- Refactor: The employees table stores both current and former employees.
-- Create a table inheritance structure:
-- - employees (base table - as is)
-- - employees_current INHERITS (employees) - active employees
-- - employees_archive INHERITS (employees) - inactive employees
--
-- Migrate data accordingly. Discuss pros/cons vs. partitioning vs. views.
--
-- HINT: PostgreSQL table inheritance is different from partitioning.
-- Think about: Do queries on parent table include child table rows?
-- Yes, by default. Use ONLY keyword to query parent only.
-- Discuss: Most modern PostgreSQL favors declarative partitioning over inheritance.


-- =============================================================================
-- SECTION 3: Views & Materialized Views
-- =============================================================================

-- Q3.1 🟢 Easy
-- Create a view 'v_product_catalog' that shows:
-- product_name, category hierarchy path, supplier, price, stock status
-- (In Stock / Low Stock / Out of Stock based on units_in_stock vs reorder_level).
-- HINT: Standard CREATE VIEW with JOINs and CASE WHEN.


-- Q3.2 🟡 Medium
-- Create a MATERIALIZED VIEW 'mv_monthly_sales_summary' that pre-computes:
-- year, month, category, total_orders, total_revenue, avg_order_value,
-- unique_customers.
-- Show how to refresh it and discuss when to use materialized vs regular views.
--
-- HINT: CREATE MATERIALIZED VIEW mv_monthly_sales_summary AS SELECT ...;
-- REFRESH MATERIALIZED VIEW mv_monthly_sales_summary;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_monthly_sales_summary; 
-- (needs a UNIQUE index on the materialized view for CONCURRENTLY)
--
-- Discuss: 
-- Regular view = re-runs query every time = always fresh, can be slow.
-- Materialized view = cached result = fast reads, needs manual refresh.


-- Q3.3 🔴 Hard
-- Create an updatable view 'v_active_employees' that:
-- Only shows active employees (is_active = TRUE).
-- Allows INSERT/UPDATE through the view.
-- Ensures any INSERT through the view sets is_active = TRUE (WITH CHECK OPTION).
--
-- HINT: CREATE VIEW v_active_employees AS
-- SELECT * FROM employees WHERE is_active = TRUE
-- WITH CHECK OPTION;
--
-- Test: Try to INSERT an employee with is_active = FALSE through the view.
-- What happens? The WITH CHECK OPTION prevents it.
-- Discuss: WITH LOCAL CHECK OPTION vs WITH CASCADED CHECK OPTION for nested views.


-- =============================================================================
-- SECTION 4: Indexes
-- =============================================================================

-- Q4.1 🟢 Easy
-- Create appropriate indexes to speed up these common queries:
-- 1. Searching products by name (partial match with LIKE)
-- 2. Finding orders by date range
-- 3. Looking up employees by department and salary
--
-- HINT: 
-- B-tree for exact match and range queries.
-- pg_trgm GIN index for LIKE '%pattern%' (trigram matching).
-- Composite index (dept_id, salary) for multi-column filters.
-- Think about column order in composite indexes!


-- Q4.2 🟡 Medium
-- Create a partial index on orders for 'pending' status only.
-- Discuss why this is more efficient than indexing the entire status column.
-- Verify with EXPLAIN ANALYZE.
--
-- HINT: CREATE INDEX idx_orders_pending ON orders(order_date) WHERE status = 'pending';
-- This index is tiny because it only contains pending orders.
-- Queries filtering WHERE status = 'pending' AND order_date > '...' use this index.
-- Full status index would include all rows - much larger and slower to maintain.


-- Q4.3 🔴 Hard
-- Create expression indexes for:
-- 1. Case-insensitive email search: LOWER(email)
-- 2. Year extraction from order_date: EXTRACT(YEAR FROM order_date)
-- 3. Computed profit margin: (unit_price - cost_price) / unit_price
--
-- Verify each with EXPLAIN ANALYZE showing index usage.
--
-- HINT: CREATE INDEX idx_customers_email_lower ON customers(LOWER(email));
-- The query must use the SAME expression: WHERE LOWER(email) = 'xxx'
-- If you write WHERE email = 'xxx', the index won't be used!
-- Discuss: Why do expression indexes exist? When are they better than 
-- storing the computed value in a separate column?
