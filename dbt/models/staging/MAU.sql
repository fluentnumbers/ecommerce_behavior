-- MAU(Monthly Activated User) trend grouped by month, event_type

select *
from (select format_date('%Y-%m', event_time) as month, event_type, count(distinct user_id) as cnt
    from oct_19
    group by month, event_type
    union
    select format_date('%Y-%m', event_time) as month, event_type, count(distinct user_id) as cnt
    from nov_19
    group by month, event_type
    union
    select format_date('%Y-%m', event_time) as month, event_type, count(distinct user_id) as cnt
    from dec_19
    group by month, event_type
    union
    select format_date('%Y-%m', event_time) as month, event_type, count(distinct user_id) as cnt
    from jan_20
    group by month, event_type
    union
    select format_date('%Y-%m', event_time) as month, event_type, count(distinct user_id) as cnt
    from feb_20
    group by month, event_type) as t
