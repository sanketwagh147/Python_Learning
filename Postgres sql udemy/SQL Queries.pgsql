-- Q2
-- select name, membercost from cd.facilities

--Q3
-- select * from  cd.facilities
-- where membercost>0

--Q4
-- select facid, name, membercost, monthlymaintenance
-- from cd.facilities
-- where membercost > 0 and membercost < monthlymaintenance/50

--Q5
-- select * from cd.facilities
-- where name like '%Tennis%'

--Q6
-- select * from cd.facilities
-- where facid in (1,5)

-- Q7
-- select memid, surname, firstname, joindate
-- from cd.members
-- where joindate > '2012-09-01'

--Q8
-- select distinct surname
-- from cd.members
-- order by surname
-- limit 10

--Q9
-- select date(max(joindate))
-- from cd.members

--Q10
-- select count(*)
-- from cd.facilities
-- WHERE guestcost > 10

--Q11
-- select extract(month from starttime) from cd.bookings
-- select facid, slots 
-- from cd.bookings
-- where 9 = extract(MONTH from starttime)
-- and extract(year from starttime) = 2012

--Q12
-- select facid, sum(slots)
-- from cd.bookings
-- where starttime >= '2012-09-01' and starttime <= '2012-10-01'
-- group by facid
-- order by sum(slots)

--Q13
-- select facid, sum(slots)
-- from cd.bookings
-- group by facid
-- HAVING sum(slots) > 1000
-- order by facid

--Q13
-- select to_char(date(starttime),'YY-MM-DD') as start, name
-- from cd.facilities
-- inner join cd.bookings
-- on cd.bookings.facid = cd.facilities.facid
-- where name like 'Tennis %' and to_char(date(starttime),'YY-MM-DD') = '12-09-21'

--Q14
select starttime,firstname, surname
from cd.bookings
inner join cd.members
on cd.bookings.memid = cd.members.memid
where firstname like 'David' and surname like 'Farrell'