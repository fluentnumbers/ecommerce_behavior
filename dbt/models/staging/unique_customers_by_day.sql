-- Number of unique customer visited our shop by day

select format_date('%m-%d', event_time) as day, count(distinct user_id) as daily_visitor
from {{ source("staging", "data") }}
group by day
