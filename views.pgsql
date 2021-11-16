-- create view customer_view as 
-- select first_name, last_name, address from customer
-- inner join address
-- on customer.address_id = address.address_id;

-- select * from customer_view
-- create or replace view customer_view as 
-- select first_name, last_name, address, district from customer
-- inner join address
-- on customer.address_id = address.address_id;

-- --Drop VIEW
-- drop view customer_view

--Check if view EXISTS
-- drop view if exists customer_view

--Rename VIEW
-- alter view customer_view rename to customer_info

