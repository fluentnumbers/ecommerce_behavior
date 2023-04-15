-- Daily traffic 
select format_date('%m-%d', event_time) as day, count(distinct user_session) as traffic
from {{source("staging","data")}}
group by day