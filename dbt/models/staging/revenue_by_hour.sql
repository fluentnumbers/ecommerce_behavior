-- Accumulated revenue by hour

select format_date('%H', event_time) as hour, sum(price) as revenue
from {{ source("staging", "data") }}
where event_type = 'purchase'
group by hour
