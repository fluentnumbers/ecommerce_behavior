{{
    config(
        materialized="table",
    )
}}

with
    daily_customers as (
        select
            format_date("%y-%m-%d", event_time) as day,
            count(distinct user_id) as daily_visitor
        from {{ source("ecommerce-behavior", "data") }}
        group by day
    )
select *
from daily_customers

    
