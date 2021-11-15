SELECT 
sum(case rental_rate
    when 0.99 then 1
    else 0
end) as number_of_bargains,
sum(case rental_rate
    when 2.99 then 1
    else 0
end) as regular ,
sum(case rental_rate
    when 4.99 then 1
    else 0
end) as premium
from film