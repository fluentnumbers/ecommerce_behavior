-- Daily traffic 
{{
    config(
        materialized="table",
    )
}}
select format_date('%m-%d', event_time) as day, count(distinct user_session) as traffic
from {{source("ecommerce-behavior","data")}}
group by day