create or replace view failure as
    select date(time) date, count(status)
    from log
    where status != '200 OK'
    group by date(time)
    order by date(time);

create or replace view total_access as
    select date(time) date, count(status)
    from log
    group by date(time)
    order by date(time);
