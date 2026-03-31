-- =============================================================================
-- DQL (Data Query Language) Practice Problems
-- Database: postgresql://sanket@localhost:5432/local_db
-- 
-- 90% of real-world SQL is SELECT queries. Master these thoroughly.
-- Difficulty: 🟢 Easy  🟡 Medium  🔴 Hard
-- =============================================================================


-- =============================================================================
-- SECTION 1: SELECT Basics & Filtering (WHERE, IN, BETWEEN, LIKE, IS NULL)
-- =============================================================================

-- Q1.1 🟢 Easy
-- List all active employees with their full name, job title, and salary.
-- Sort by salary descending.
-- HINT: Concatenate first_name and last_name. Use WHERE for filtering.


-- Q1.2 🟡 Medium
-- Find all employees who were hired in 2021, earn between 50000 and 90000,
-- and work in either Engineering or Marketing departments.
-- Show: full name, hire_date, salary, department name.
-- HINT: You need a JOIN with departments. Use BETWEEN for salary and 
-- EXTRACT(YEAR FROM hire_date) for year filtering.


-- Q1.3 🔴 Hard
-- Find employees whose email domain is 'company.com', who have a commission 
-- percentage set, AND whose total compensation (salary + salary * commission_pct)
-- exceeds the average salary of their own department.
-- Show: full name, department, salary, commission, total compensation, dept avg salary.
-- HINT: Think about correlated subquery or CTE with department averages.
-- You'll need to handle NULL commission with COALESCE.


-- =============================================================================
-- SECTION 2: Aggregate Functions (COUNT, SUM, AVG, MIN, MAX)
-- =============================================================================

-- Q2.1 🟢 Easy
-- For each department, find the number of employees, average salary, 
-- minimum salary, and maximum salary. Only include departments with 
-- more than 2 employees.
-- HINT: GROUP BY + HAVING. Join with departments for names.


-- Q2.2 🟡 Medium
-- Find the total revenue generated per product category in 2024.
-- Show: category name, total items sold, total revenue (quantity * unit_price * (1 - discount/100)).
-- Only include categories with total revenue > 50000.
-- Sort by total revenue descending.
-- HINT: Multi-table JOIN: order_items -> products -> categories -> orders.
-- Filter orders by year. Apply the discount calculation carefully.


-- Q2.3 🔴 Hard
-- Calculate the Month-over-Month (MoM) revenue growth percentage for 2024.
-- Show: month, total_revenue, previous_month_revenue, growth_percentage.
-- HINT: Use DATE_TRUNC to group by month. Use LAG() window function
-- to get previous month's value. Growth = ((current - previous) / previous) * 100.
-- Consider what happens for the first month (no previous data).


-- =============================================================================
-- SECTION 3: JOINs (INNER, LEFT, RIGHT, FULL, CROSS, SELF)
-- =============================================================================

-- Q3.1 🟢 Easy
-- List all products along with their category name and supplier company name.
-- Include products even if they don't have a supplier (LEFT JOIN).
-- Sort by category, then product name.
-- HINT: JOIN products with categories and suppliers. Think about which 
-- table should be the LEFT table.


-- Q3.2 🟡 Medium
-- Find customers who have placed orders but never left a review for any product.
-- Show: customer name, email, total orders placed, total amount spent.
-- HINT: LEFT JOIN customers with reviews, then filter WHERE review is NULL.
-- Join with orders and order_items for order/spending data.


-- Q3.3 🟡 Medium
-- Show the employee hierarchy: For each employee, display their name, 
-- their manager's name, and their manager's manager's name (skip-level manager).
-- HINT: Self-JOIN employees table multiple times. Use LEFT JOIN since 
-- top-level managers don't have a manager.
-- Think: e JOIN e AS mgr ON e.manager_id = mgr.emp_id
--        LEFT JOIN e AS skip ON mgr.manager_id = skip.emp_id


-- Q3.4 🔴 Hard
-- Find all pairs of products that have been bought together in the same order
-- more than 2 times. Show product1_name, product2_name, times_bought_together.
-- HINT: Self-join order_items to itself ON same order_id but different product_id.
-- To avoid duplicate pairs (A,B) and (B,A), use WHERE oi1.product_id < oi2.product_id.
-- GROUP BY the pair and HAVING count > 2.


-- Q3.5 🔴 Hard
-- For each department, find the employee who has worked the most total hours
-- across all projects. Show: department, employee name, total hours.
-- If a department has no employees assigned to projects, still show it with NULLs.
-- HINT: LEFT JOIN departments -> employees -> employee_projects.
-- Use a window function (ROW_NUMBER / RANK) partitioned by department
-- to pick the top employee per department.


-- =============================================================================
-- SECTION 4: Subqueries (Scalar, Row, Table, Correlated)
-- =============================================================================

-- Q4.1 🟢 Easy
-- Find all products whose unit_price is above the average unit_price of all products.
-- Show: product name, price, and how much above average it is.
-- HINT: Subquery in WHERE or calculate avg in a CTE.


-- Q4.2 🟡 Medium
-- Find the most expensive product in each category.
-- Show: category name, product name, unit_price.
-- HINT: Use a correlated subquery in WHERE:
-- WHERE p.unit_price = (SELECT MAX(unit_price) FROM products WHERE category_id = p.category_id)
-- OR use ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY unit_price DESC)


-- Q4.3 🟡 Medium
-- Find customers who have spent more than the average customer spending.
-- Show: customer name, total_spent, avg_customer_spent, difference.
-- HINT: First calculate total per customer, then compare to the average of those totals.
-- This is a two-level aggregation problem.


-- Q4.4 🔴 Hard
-- For each product, determine if its sales are "Above Average", "Below Average", 
-- or "No Sales" compared to the average sales quantity across all products that 
-- have been sold at least once.
-- Show: product_name, total_qty_sold, avg_qty_all_products, classification.
-- HINT: Use a CTE to calculate per-product totals first.
-- Then use a scalar subquery for the average.
-- Use CASE WHEN for the classification.
-- LEFT JOIN products with the CTE to catch "No Sales" products.


-- Q4.5 🔴 Hard
-- Find the "loyal customers" - customers whose EVERY order has been delivered
-- (not a single cancelled or returned order). Exclude customers with 0 orders.
-- Show: customer name, total orders, earliest order, latest order.
-- HINT: Think about NOT EXISTS with a subquery checking for non-delivered orders.
-- OR: count total orders = count delivered orders per customer.
-- Which approach is more efficient and why?


-- =============================================================================
-- SECTION 5: Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG, 
--                              NTILE, FIRST_VALUE, LAST_VALUE, NTH_VALUE)
-- =============================================================================

-- Q5.1 🟢 Easy
-- Rank all employees by salary within their department.
-- Show: department name, employee name, salary, rank_in_dept.
-- HINT: RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC).
-- Think about: What's the difference between RANK, DENSE_RANK, and ROW_NUMBER
-- when salaries are tied?


-- Q5.2 🟡 Medium
-- For each order, show the running total of revenue for that customer over time.
-- Show: customer name, order_id, order_date, order_total, running_total.
-- HINT: First calculate order totals using a CTE with order_items.
-- Then use SUM() OVER (PARTITION BY customer_id ORDER BY order_date 
--                       ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)


-- Q5.3 🟡 Medium
-- Divide products into 4 price quartiles using NTILE.
-- For each quartile, show: quartile number, count of products, 
-- min price, max price, avg price.
-- HINT: Use NTILE(4) OVER (ORDER BY unit_price) in a CTE first,
-- then GROUP BY quartile number.


-- Q5.4 🔴 Hard
-- For each product, show the gap in days between consecutive orders.
-- Show: product name, order_date, previous_order_date, gap_in_days.
-- Flag products with an average gap > 60 days as "slow_moving".
-- HINT: LAG(order_date) OVER (PARTITION BY product_id ORDER BY order_date).
-- Use DATE_PART('day', order_date - prev_order_date) for gap.
-- Final aggregation to classify products.


-- Q5.5 🔴 Hard
-- Calculate the "market basket" analysis: For each order, show what percentage
-- of the total order value each item represents, AND its percentage of 
-- the overall category revenue.
-- Show: order_id, product_name, category_name, item_total, 
--        pct_of_order, pct_of_category_revenue.
-- HINT: Use multiple window functions:
-- SUM(item_total) OVER (PARTITION BY order_id) for order total
-- SUM(item_total) OVER (PARTITION BY category_id) for category total
-- Then calculate percentages.


-- Q5.6 🔴 Hard (Interview Favorite)
-- Find the top 3 products by revenue in each category, BUT if two products
-- have the same revenue, both should get the same rank and the next rank 
-- should be skipped (standard competition ranking).
-- Show: category, rank, product_name, total_revenue.
-- HINT: Use DENSE_RANK() vs RANK() here - which one is correct for 
-- "competition ranking"? Think carefully.
-- Filter using a subquery or CTE with WHERE rank <= 3.


-- =============================================================================
-- SECTION 6: CTEs (Common Table Expressions) & Recursive CTEs
-- =============================================================================

-- Q6.1 🟢 Easy
-- Using a CTE, find departments where the total salary expenditure 
-- exceeds their budget.
-- Show: department name, total_salary_expense, budget, overspend_amount.
-- HINT: CTE to sum salaries per department, then join with departments.


-- Q6.2 🟡 Medium
-- Using multiple CTEs, find the "best value" products - products with 
-- high ratings (avg >= 4) and high sales volume (top 25%).
-- Show: product name, avg_rating, review_count, total_sold, revenue.
-- HINT: CTE1 = rating stats, CTE2 = sales stats, CTE3 = percentile calc.
-- Join them together and filter.


-- Q6.3 🔴 Hard
-- Write a RECURSIVE CTE to display the full employee hierarchy as a tree.
-- Show: emp_name, job_title, manager_name, level, full_path.
-- full_path should look like: "Rajesh Kumar > Neha Gupta > Sanjay Tiwari"
-- HINT: 
-- Base case: employees WHERE manager_id IS NULL (top-level)
-- Recursive case: JOIN employees ON e.manager_id = cte.emp_id
-- Build the path using string concatenation: parent_path || ' > ' || name
-- Level starts at 1 and increments.


-- Q6.4 🔴 Hard
-- Using a recursive CTE, build the full category hierarchy path.
-- Then for each leaf category (no children), calculate total revenue.
-- Show: full_category_path, total_products, total_revenue.
-- HINT: Recursive CTE for category tree (similar to employee hierarchy).
-- Leaf categories = categories NOT IN (SELECT parent_category_id FROM categories WHERE parent_category_id IS NOT NULL)
-- Join with products and order_items for revenue.


-- =============================================================================
-- SECTION 7: String Functions & Date Functions
-- =============================================================================

-- Q7.1 🟢 Easy
-- Extract and display employee information in a formatted way:
-- "Mr./Ms. LASTNAME, Firstname - hired X years ago"
-- Show the hire duration in years and months.
-- HINT: UPPER(), INITCAP(), AGE(), DATE_PART().
-- For Mr./Ms., you can make assumptions or skip the prefix.


-- Q7.2 🟡 Medium
-- Parse customer email addresses: extract the username (before @) and 
-- domain (after @). Find which email domains are most common.
-- Show: domain, customer_count, list of usernames (comma-separated).
-- HINT: SPLIT_PART(email, '@', 1) for username, SPLIT_PART(email, '@', 2) for domain.
-- STRING_AGG(username, ', ') for comma-separated list.


-- Q7.3 🔴 Hard
-- Create a sales calendar report for 2024: For each month, show the 
-- revenue, but also show months with zero orders (fill gaps).
-- Show: month_name, year, order_count, revenue (0 if no orders).
-- HINT: Use GENERATE_SERIES to create all months of 2024.
-- LEFT JOIN with orders. TO_CHAR for month name formatting.
-- COALESCE for zero-filling.


-- =============================================================================
-- SECTION 8: CASE WHEN, COALESCE, NULLIF, GREATEST, LEAST
-- =============================================================================

-- Q8.1 🟢 Easy
-- Classify employees into salary bands: 
-- Below 50K = "Entry Level", 50K-100K = "Mid Level", 
-- 100K-150K = "Senior Level", Above 150K = "Executive Level"
-- Show: employee name, salary, band, department.
-- HINT: CASE WHEN with ranges.


-- Q8.2 🟡 Medium
-- Create an order summary that shows:
-- customer name, order status (with friendly labels), 
-- estimated_delivery = shipped_date + 3 days (if shipped),
-- delay_flag = 'DELAYED' if delivered_date > shipped_date + 5 days, else 'ON TIME'
-- For pending/cancelled orders, show 'N/A' for delivery fields.
-- HINT: Use CASE WHEN for status labels and conditional logic.
-- COALESCE for NULL handling. Date arithmetic with INTERVAL.


-- Q8.3 🔴 Hard
-- Build a product profitability analysis:
-- profit_margin = (unit_price - cost_price) / unit_price * 100
-- But some products have NULL cost_price. Handle that.
-- Classify: margin > 60% = "High Margin", 40-60% = "Medium", 
-- 20-40% = "Low", < 20% = "Loss Leader", NULL cost = "Unknown"
-- Also factor in: if the product is discontinued AND has stock > 0 = "Dead Stock"
-- Show: product_name, prices, margin%, classification, dead_stock_flag.
-- HINT: Nested CASE WHEN. NULLIF to avoid division by zero.
-- Multiple conditions need careful ordering in CASE WHEN.


-- =============================================================================
-- SECTION 9: Set Operations (UNION, INTERSECT, EXCEPT)
-- =============================================================================

-- Q9.1 🟢 Easy
-- Find all cities that appear in either the customers table or 
-- the suppliers table (combined unique list).
-- HINT: UNION automatically removes duplicates. UNION ALL keeps them.


-- Q9.2 🟡 Medium
-- Find products that have been reviewed but never ordered, AND
-- products that have been ordered but never reviewed.
-- Show them in a single result with a column indicating which case.
-- HINT: Use EXCEPT to find differences in both directions.
-- Then UNION the two results with a label column.


-- Q9.3 🔴 Hard
-- Find customers who have bought products from ALL product categories
-- that have at least one product (i.e., "universal buyers").
-- HINT: This is relational division. One approach:
-- Count distinct categories per customer from their orders.
-- Compare with total number of categories that have products.
-- EXCEPT approach: For each customer, find categories they HAVEN'T bought from.
-- If that set is empty, they're a universal buyer.


-- =============================================================================
-- SECTION 10: EXISTS, ANY, ALL
-- =============================================================================

-- Q10.1 🟢 Easy
-- Find departments that have at least one employee earning more than 150000.
-- HINT: Use EXISTS with a correlated subquery.
-- Compare with the IN approach: WHERE dept_id IN (SELECT dept_id FROM employees WHERE salary > 150000)
-- Think about which one performs better and why.


-- Q10.2 🟡 Medium
-- Find products whose unit_price is greater than ALL products in the 
-- 'Books' parent category (including Fiction and Non-Fiction subcategories).
-- HINT: Use ALL with a subquery. First find all category_ids under 'Books'.
-- > ALL means greater than every single value in the subquery result.


-- Q10.3 🔴 Hard
-- Find customers who have placed an order in EVERY quarter of 2024
-- (Q1: Jan-Mar, Q2: Apr-Jun, Q3: Jul-Sep, Q4: Oct-Dec).
-- HINT: For each customer, check that there does NOT EXIST a quarter
-- where they have no orders.
-- Use GENERATE_SERIES(1,4) for quarters.
-- For each quarter, check EXISTS of order in that date range.
-- Double NOT EXISTS = "for all" in relational algebra.


-- =============================================================================
-- SECTION 11: GROUP BY Variations (GROUPING SETS, CUBE, ROLLUP)
-- =============================================================================

-- Q11.1 🟢 Easy
-- Create a sales summary report using ROLLUP:
-- Show revenue by category, and within category by product, 
-- with subtotals for each category and a grand total.
-- HINT: GROUP BY ROLLUP(category_name, product_name).
-- NULLs in the grouping columns indicate subtotal/total rows.


-- Q11.2 🟡 Medium
-- Create a cross-analysis report using CUBE:
-- Revenue by payment_method AND order_status, with all possible subtotals.
-- Show: payment_method, status, order_count, total_revenue.
-- HINT: GROUP BY CUBE(payment_method, status).
-- Use GROUPING() function to identify which rows are subtotals.


-- Q11.3 🔴 Hard
-- Create a GROUPING SETS report that shows:
-- 1. Revenue by year and quarter
-- 2. Revenue by year and payment method  
-- 3. Grand total
-- All in a single query. Label each row with its "report_type".
-- HINT: GROUPING SETS ((year, quarter), (year, payment_method), ())
-- Use CASE WHEN with GROUPING() to create report_type labels.
-- GROUPING(column) returns 1 if column is aggregated (part of a subtotal).


-- =============================================================================
-- SECTION 12: Advanced Patterns & Real-World Scenarios
-- =============================================================================

-- Q12.1 🟡 Medium - "Gaps and Islands Problem"
-- Find consecutive months where a customer placed at least one order.
-- Show: customer_name, streak_start, streak_end, streak_length_months.
-- HINT: This is the classic "gaps and islands" problem.
-- Assign row numbers to months, subtract from month number.
-- Consecutive months will have the same difference (island identifier).


-- Q12.2 🔴 Hard - "Cohort Analysis"
-- Perform a customer retention cohort analysis:
-- Group customers by their registration quarter (cohort).
-- For each cohort, calculate what percentage of customers placed orders
-- in each subsequent quarter.
-- Show: cohort_quarter, months_since_registration, active_customers, retention_rate%.
-- HINT: CTE1 = assign cohort. CTE2 = find order quarters per customer.
-- Cross-join cohorts with time periods, then left join with actual activity.


-- Q12.3 🔴 Hard - "Median Calculation"
-- Calculate the median order value per customer tier (premium vs non-premium).
-- PostgreSQL has PERCENTILE_CONT but understanding the manual approach is key.
-- Show: tier, median_order_value, mean_order_value, count.
-- HINT: Use PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY order_total).
-- Also try implementing it manually using ROW_NUMBER and COUNT:
-- Find the middle row(s) in the ordered list INSIDE a window.


-- Q12.4 🔴 Hard - "Funnel Analysis"
-- Track the customer journey funnel:
-- Step 1: Registered (all customers)
-- Step 2: First order placed
-- Step 3: Second order placed
-- Step 4: Left a review
-- Step 5: Became premium
-- For each step, show count and drop-off percentage from previous step.
-- HINT: Use CTEs for each funnel step. 
-- Step 2: EXISTS in orders. Step 3: COUNT in orders >= 2.
-- Calculate drop-off: (previous_step - current_step) / previous_step * 100.


-- Q12.5 🔴 Hard - "Year-over-Year Comparison" (Interview Classic)
-- Compare 2023 vs 2024 performance by category:
-- Show: category, revenue_2023, revenue_2024, yoy_growth%, 
--        orders_2023, orders_2024, avg_order_value change.
-- Highlight categories that grew > 50% and those that declined.
-- HINT: Separate CTEs for 2023 and 2024 aggregations.
-- FULL OUTER JOIN on category to catch categories only active in one year.
-- COALESCE(revenue, 0) for missing years.


-- =============================================================================
-- BONUS: 3 Interview-Level Advanced Problems
-- =============================================================================

-- Q_INT1 🔴🔴 Interview Level - "Second Highest Salary per Department"
-- For each department, find the employee with the second-highest salary.
-- If there's no second-highest (only 1 employee), show NULL.
-- If there's a tie for first, the second-highest should be lower than tied first.
-- Show: department, emp_name, salary, highest_salary_in_dept.
-- 
-- THOUGHT PROCESS:
-- This tests DENSE_RANK/ROW_NUMBER understanding.
-- Key trap: RANK vs DENSE_RANK matters when there are ties.
-- If two employees tie for #1 salary, RANK gives #3 to the next person,
-- but DENSE_RANK gives #2. We want DENSE_RANK = 2 (the actual second distinct salary).
-- 
-- Approach: CTE with DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC)
-- Filter where dense_rank = 2. LEFT JOIN back to departments to show NULL
-- for departments without a second-highest.
--
-- Edge case: Department with all employees having same salary -> no rank 2.


-- Q_INT2 🔴🔴 Interview Level - "Running Sum with Reset"
-- Calculate the running total of order amounts per customer, BUT reset 
-- the running total back to 0 whenever a customer's order is cancelled or returned.
-- Show: customer, order_date, order_total, running_total_with_reset.
--
-- THOUGHT PROCESS:
-- Standard window functions can't "reset". This needs a creative approach.
-- Strategy: Create "groups" that increment every time there's a reset event.
-- 1. Flag cancellations/returns with a 1, others with 0.
-- 2. Use a cumulative SUM of flags to create group identifiers.
-- 3. Then do running SUM within each group.
--
-- Key insight: SUM(reset_flag) OVER (PARTITION BY customer_id ORDER BY order_date 
--              ROWS UNBOUNDED PRECEDING) creates group numbers.
-- Then: SUM(order_total) OVER (PARTITION BY customer_id, group_num 
--        ORDER BY order_date ROWS UNBOUNDED PRECEDING)


-- Q_INT3 🔴🔴 Interview Level - "Pivot Table: Monthly Revenue by Category"
-- Create a pivot table showing categories as rows and months as columns
-- for 2024. Each cell = revenue. Include row totals and column totals.
--
-- THOUGHT PROCESS:
-- PostgreSQL doesn't have native PIVOT. Use conditional aggregation.
-- SUM(CASE WHEN month = 1 THEN revenue ELSE 0 END) AS jan_revenue
-- 
-- Approach:
-- 1. CTE: Calculate monthly revenue per category from orders + order_items + products.
-- 2. Conditional aggregation with 12 CASE WHEN statements.
-- 3. ROLLUP for row totals row.
-- 4. SUM without partition for column totals.
-- 
-- Alternative: Use crosstab() from tablefunc extension (mention but preferred
-- to solve with standard SQL for interviews).
-- 
-- KEY INSIGHT: The column headers (months) must be known at query-write time.
-- For truly dynamic pivoting, you need dynamic SQL (EXECUTE in PL/pgSQL).
