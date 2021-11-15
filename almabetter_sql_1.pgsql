-- select customer_id,sum(amount) from payment 
-- where staff_id = 2
-- group by customer_id
-- having sum(amount) > 110

-- select count(title) from film
-- where title like 'J%' 

select customer_id,first_name, address_id from customer 
where address_id < 500 and first_name like 'E%'
group by customer_id
having customer_id = max(customer_id)
order by customer_id desc
limit 1
