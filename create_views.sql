create or replace view failure as
    select date(time) date, count(status)
    from log
    where status not like '200%'
    group by date(time)
    order by date(time);

create or replace view total_access as
    select date(time) date, count(status)
    from log
    group by date(time)
    order by date(time);
