-- select * from customer

--Case

-- select customer_id,
-- CASE
--     when (customer_id <= 100) then 'Premium'
--     when (customer_id between 100 and 200) then 'Plus'
--     else 'Normal'

-- END as customer_class

-- from customer
-- order by customer_id

select customer_id,
case customer_id
    when 2 then 'Winner'
    when 5 then 'Second Place'
    else 'Normal'
end as raffle_results    
from customer