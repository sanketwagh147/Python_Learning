-- =============================================================================
-- Query Optimization & Performance Practice Problems
-- Database: postgresql://sanket@localhost:5432/local_db
-- 
-- Understanding EXPLAIN ANALYZE, indexes, query patterns.
-- These problems focus on WHY some queries are slow and HOW to fix them.
-- Difficulty: 🟢 Easy  🟡 Medium  🔴 Hard
-- =============================================================================


-- =============================================================================
-- HOW TO USE EXPLAIN ANALYZE
-- =============================================================================
-- Always prefix your queries with:
--   EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) <your query>
--
-- Key metrics to understand:
-- - Seq Scan = full table scan (bad for large tables)
-- - Index Scan / Index Only Scan = using index (good)
-- - Nested Loop / Hash Join / Merge Join = join strategies
-- - actual time = real execution time
-- - rows = actual vs estimated rows (big difference = bad stats)
-- - Buffers: shared hit = from cache, shared read = from disk


-- =============================================================================
-- SECTION 1: Identifying Slow Queries
-- =============================================================================

-- Q1.1 🟢 Easy
-- Run EXPLAIN ANALYZE on this query and identify the bottleneck:
--
-- SELECT * FROM products WHERE LOWER(product_name) LIKE '%samsung%';
--
-- Why is it slow? How would you fix it?
-- HINT: Check if there's a Seq Scan. Why can't a regular B-tree index help
-- with LIKE '%pattern%'? Think about: trigram index (pg_trgm extension)
-- or expression index on LOWER(product_name).


-- Q1.2 🟡 Medium
-- Analyze and optimize this query:
--
-- SELECT c.first_name, c.last_name, 
--        (SELECT COUNT(*) FROM orders o WHERE o.customer_id = c.customer_id) as order_count,
--        (SELECT SUM(oi.quantity * oi.unit_price) FROM order_items oi 
--         JOIN orders o ON oi.order_id = o.order_id 
--         WHERE o.customer_id = c.customer_id) as total_spent
-- FROM customers c
-- ORDER BY total_spent DESC;
--
-- Problem: How many times does each subquery execute?
-- HINT: Correlated subqueries execute once PER ROW in the outer query.
-- With 25 customers, each subquery runs 25 times = 50 total sub-executions.
-- 
-- Fix: Rewrite using JOINs and GROUP BY or LEFT JOIN with pre-aggregated CTEs.
-- The join-based version scans orders and order_items only ONCE.


-- Q1.3 🔴 Hard
-- Profile this complex report query and optimize it:
--
-- SELECT 
--   d.dept_name,
--   e.first_name || ' ' || e.last_name as emp_name,
--   e.salary,
--   (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id) as dept_avg,
--   (SELECT COUNT(*) FROM employee_projects WHERE emp_id = e.emp_id) as project_count,
--   (SELECT SUM(hours_worked) FROM employee_projects WHERE emp_id = e.emp_id) as total_hours,
--   (SELECT MAX(new_salary) - MIN(old_salary) FROM salary_history WHERE emp_id = e.emp_id) as salary_growth
-- FROM employees e
-- JOIN departments d ON e.dept_id = d.dept_id
-- WHERE e.is_active = TRUE;
--
-- Count the number of correlated subqueries and their impact.
-- Rewrite using window functions and CTEs to minimize scans.
-- HINT: 
-- dept_avg -> AVG(salary) OVER (PARTITION BY dept_id)
-- project stats -> CTE with GROUP BY emp_id
-- salary growth -> CTE with GROUP BY emp_id
-- Final query joins these pre-computed CTEs.


-- =============================================================================
-- SECTION 2: Index Optimization
-- =============================================================================

-- Q2.1 🟢 Easy
-- This query needs optimization. Create the right index:
--
-- SELECT * FROM orders 
-- WHERE customer_id = 5 AND status = 'delivered' 
-- ORDER BY order_date DESC;
--
-- HINT: A composite index on (customer_id, status, order_date DESC)
-- covers the WHERE clause and ORDER BY in a single index scan.
-- Discuss: Does column order in the composite index matter? YES!
-- The leftmost columns should be the equality conditions (=),
-- range/order conditions should come last.


-- Q2.2 🟡 Medium
-- Which of these indexes would be used for this query? Why?
--
-- CREATE INDEX idx_a ON order_items(order_id);
-- CREATE INDEX idx_b ON order_items(product_id, order_id);
-- CREATE INDEX idx_c ON order_items(order_id, product_id, quantity);
--
-- Query: SELECT order_id, product_id, quantity 
--        FROM order_items WHERE order_id = 42;
--
-- HINT: idx_c would give an "Index Only Scan" because it contains all 
-- columns needed (covering index). The query never needs to visit the 
-- table heap. idx_a would need a heap lookup for product_id and quantity.
-- Discuss: The trade-off is index size vs query performance.


-- Q2.3 🔴 Hard
-- The following query pattern is used in pagination. Optimize it:
--
-- -- Page 100 with 20 items per page (skip 1980 rows)
-- SELECT * FROM products ORDER BY product_id LIMIT 20 OFFSET 1980;
--
-- What's wrong with large OFFSET values? How to fix?
-- HINT: With OFFSET 1980, PostgreSQL must scan and discard 1980 rows!
-- 
-- Better approach: "Keyset pagination" (also called "seek method"):
-- SELECT * FROM products WHERE product_id > <last_seen_id> ORDER BY product_id LIMIT 20;
-- 
-- This uses the index directly to start at the right position.
-- Trade-off: You can't jump to arbitrary pages, only next/previous.
-- Discuss: When is OFFSET okay vs when is keyset pagination essential?


-- =============================================================================
-- SECTION 3: Join Optimization
-- =============================================================================

-- Q3.1 🟡 Medium
-- Compare these two approaches for finding "customers with expensive orders":
--
-- Approach A (Subquery):
-- SELECT * FROM customers WHERE customer_id IN 
--   (SELECT customer_id FROM orders o JOIN order_items oi ON o.order_id = oi.order_id
--    GROUP BY customer_id HAVING SUM(oi.quantity * oi.unit_price) > 100000);
--
-- Approach B (JOIN):
-- SELECT c.* FROM customers c
-- JOIN orders o ON c.customer_id = o.customer_id
-- JOIN order_items oi ON o.order_id = oi.order_id
-- GROUP BY c.customer_id, c.first_name, c.last_name, c.email, c.phone, 
--          c.city, c.state, c.country, c.registration_date, c.is_premium, c.credit_limit
-- HAVING SUM(oi.quantity * oi.unit_price) > 100000;
--
-- Run EXPLAIN ANALYZE on both. Which is faster? Why?
-- HINT: Modern PostgreSQL often optimizes both to the same plan.
-- But the IN subquery approach with EXISTS can sometimes be faster
-- because it can short-circuit. Profile both and compare actual times.


-- Q3.2 🔴 Hard
-- This query generates a report but is slow on large data:
--
-- SELECT p.product_name, c.category_name,
--   COUNT(DISTINCT o.order_id) as order_count,
--   SUM(oi.quantity) as total_sold,
--   SUM(oi.quantity * oi.unit_price * (1 - oi.discount/100)) as revenue,
--   AVG(r.rating) as avg_rating,
--   COUNT(DISTINCT r.review_id) as review_count
-- FROM products p
-- LEFT JOIN categories c ON p.category_id = c.category_id
-- LEFT JOIN order_items oi ON p.product_id = oi.product_id
-- LEFT JOIN orders o ON oi.order_id = o.order_id
-- LEFT JOIN reviews r ON p.product_id = r.product_id
-- GROUP BY p.product_id, p.product_name, c.category_name;
--
-- Problem: The LEFT JOINs cause a "fan-out" effect.
-- If a product has 10 order_items and 5 reviews, the join produces 50 rows.
-- COUNT(DISTINCT) and SUM are computed over these 50 rows = wrong totals!
--
-- HINT: Fix by pre-aggregating reviews and order stats separately:
-- CTE1 = sales stats grouped by product
-- CTE2 = review stats grouped by product
-- Final: products LEFT JOIN CTE1 LEFT JOIN CTE2
-- This avoids the cartesian explosion from joining two one-to-many relationships.


-- =============================================================================
-- SECTION 4: Common Anti-Patterns
-- =============================================================================

-- Q4.1 🟡 Medium - "Functions on indexed columns"
-- This query does a Seq Scan despite having an index on order_date:
--
-- SELECT * FROM orders WHERE EXTRACT(YEAR FROM order_date) = 2024;
--
-- Why? How to fix?
-- HINT: Applying a function to an indexed column prevents index usage.
-- Fix 1: Rewrite as range condition:
--   WHERE order_date >= '2024-01-01' AND order_date < '2025-01-01'
-- Fix 2: Create an expression index:
--   CREATE INDEX idx_order_year ON orders(EXTRACT(YEAR FROM order_date));
-- Which fix is better and why? (Fix 1 - doesn't need extra index)


-- Q4.2 🟡 Medium - "SELECT * kills performance"
-- Compare these two queries:
--
-- Query A: SELECT * FROM orders WHERE status = 'pending';
-- Query B: SELECT order_id, customer_id, order_date FROM orders WHERE status = 'pending';
--
-- If there's an index on status, will Query B be faster? When?
-- HINT: If the index COVERS all needed columns, PostgreSQL can do an 
-- "Index Only Scan" and avoid reading the table at all.
-- CREATE INDEX idx_orders_status_covering ON orders(status) INCLUDE (order_id, customer_id, order_date);
-- Now Query B can use Index Only Scan. Query A still needs Heap Scan.


-- Q4.3 🔴 Hard - "N+1 Query Problem"
-- An application runs this pattern (pseudocode):
--
-- customers = SELECT * FROM customers;
-- for each customer:
--     orders = SELECT * FROM orders WHERE customer_id = ?;
--     for each order:
--         items = SELECT * FROM order_items WHERE order_id = ?;
--
-- If there are 25 customers with 40 total orders:
-- How many queries hit the database? 
-- Rewrite as a single efficient query.
--
-- HINT: 25 customers query = 1
-- 25 order queries (one per customer) = 25
-- 40 order_items queries (one per order) = 40
-- Total = 66 queries!
--
-- Fix: Single query with JOINs:
-- SELECT c.*, o.*, oi.* 
-- FROM customers c 
-- LEFT JOIN orders o ON c.customer_id = o.customer_id
-- LEFT JOIN order_items oi ON o.order_id = oi.order_id;
-- 
-- Now: 1 query. Discuss: Trade-off is data duplication in the result
-- (customer and order data repeated per item). Application must 
-- de-duplicate. ORMs handle this with "eager loading".


-- =============================================================================
-- SECTION 5: EXPLAIN Plan Reading
-- =============================================================================

-- Q5.1 🟡 Medium
-- Run this query and read the EXPLAIN output:
--
-- EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
-- SELECT e.first_name, d.dept_name, p.project_name, ep.hours_worked
-- FROM employees e
-- JOIN departments d ON e.dept_id = d.dept_id
-- JOIN employee_projects ep ON e.emp_id = ep.emp_id
-- JOIN projects p ON ep.project_id = p.project_id
-- WHERE e.salary > 100000 AND ep.hours_worked > 200;
--
-- Questions to answer from the EXPLAIN output:
-- 1. What join strategy was chosen? (Nested Loop, Hash Join, Merge Join)
-- 2. Which table is the "driving table" (scanned first)?
-- 3. Are any indexes being used?
-- 4. What's the estimated vs actual row count at each step?
-- 5. Where is the most time spent?


-- Q5.2 🔴 Hard
-- Given this plan (conceptual), identify the optimization opportunity:
--
-- Sort  (cost=500.00..510.00 rows=1000)
--   Sort Key: order_date
--   -> Hash Join  (cost=100.00..450.00 rows=1000)
--     Hash Cond: (o.customer_id = c.customer_id)
--     -> Seq Scan on orders o (cost=0.00..300.00 rows=10000)
--           Filter: (status = 'delivered')
--           Rows Removed by Filter: 9000
--     -> Hash  (cost=50.00..50.00 rows=25)
--       -> Seq Scan on customers c (cost=0.00..50.00 rows=25)
--
-- Question: Where is the biggest waste?
-- HINT: Seq Scan on orders reads 10000 rows but only needs 1000 (status = 'delivered').
-- Adding an index on orders(status) or a partial index WHERE status = 'delivered'
-- would turn the Seq Scan into an Index Scan.
-- Also: The Sort at the top could be eliminated with an index on (status, order_date).


-- Q5.3 🔴 Hard
-- PostgreSQL statistics are crucial for good plans. Demonstrate:
-- 1. Run ANALYZE on a specific table
-- 2. Check the statistics: SELECT * FROM pg_stats WHERE tablename = 'orders';
-- 3. Look at n_distinct, most_common_vals, most_common_freqs
-- 4. How does PostgreSQL use these to estimate row counts?
--
-- HINT: If most_common_vals for status shows 'delivered' with frequency 0.7,
-- PostgreSQL estimates: 10000 rows * 0.7 = 7000 rows for WHERE status = 'delivered'.
-- If the estimate is wrong (stale stats), the optimizer may choose a bad plan.
-- Fix: Run ANALYZE. Or adjust: ALTER TABLE orders ALTER COLUMN status SET STATISTICS 1000;
-- Discuss: What's the default statistics target? When would you increase it?


-- =============================================================================
-- SECTION 6: Real-World Performance Scenarios
-- =============================================================================

-- Q6.1 🔴 Hard - "Slow Dashboard Query"
-- A dashboard runs this query every 5 seconds to show real-time stats:
--
-- SELECT 
--   COUNT(*) as total_orders,
--   COUNT(*) FILTER (WHERE status = 'pending') as pending,
--   COUNT(*) FILTER (WHERE status = 'processing') as processing,
--   COUNT(*) FILTER (WHERE status = 'shipped') as shipped,
--   SUM(CASE WHEN order_date > CURRENT_TIMESTAMP - INTERVAL '1 hour' THEN 1 ELSE 0 END) as last_hour,
--   (SELECT SUM(oi.quantity * oi.unit_price) FROM order_items oi 
--    JOIN orders o2 ON oi.order_id = o2.order_id 
--    WHERE o2.order_date > CURRENT_TIMESTAMP - INTERVAL '24 hours') as daily_revenue
-- FROM orders;
--
-- With millions of orders, this is slow. How to optimize?
-- HINT: Multiple strategies:
-- 1. Materialized view refreshed every minute (not every 5 seconds)
-- 2. Approximate counts: use pg_class.reltuples for total count
-- 3. Partial indexes for status counts
-- 4. Pre-compute daily_revenue in a separate materialized view or cache table
-- 5. Use FILTER syntax (already used) instead of CASE WHEN for clarity
-- 
-- Discuss: For truly real-time dashboards, consider pg_stat_user_tables
-- or external caching (Redis) populated by triggers or CDC.
