SELECT 
sum(case rating
    when 'R' then 1
    else 0
end) as r,
sum(case rating
    when 'PG' then 1
    else 0
end) as  pg,
sum(case rating
    when 'PG-13' then 1
    else 0
end) as pg13
from film

-- select * from film
-- limit 10