-- Accumulated revenue by hour
{{
    config(
        materialized="table",
    )
}}
select format_date('%H', event_time) as hour, sum(price) as revenue
from {{ source("ecommerce-behavior", "data") }}
where event_type = 'purchase'
group by hour
