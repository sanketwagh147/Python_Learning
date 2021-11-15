-- insert into depts(
--     first_name,
--     department 
-- )
-- VALUES
-- ('Vinton', 'A'),
-- ('Lauren', 'A'),
-- ('Claire', 'B');

-- select * from depts

select (
    sum(case when department = 'A' then 1 else 0 end)/
   nullif(sum(case when department = 'B' then 1 else 0 end),0)
) as department_ratio
from depts


-- delete from depts 
-- where department = 'B'