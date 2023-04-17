-- MAU(Monthly Activated User) trend grouped by month, event_type

select *
from (select format_date('%Y-%m', event_time) as month, event_type, count(distinct user_id) as cnt
    from {{ref("data_clustered")}}
    group by month, event_type)
