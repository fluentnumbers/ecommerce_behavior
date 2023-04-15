{{
    config(
        materialized="table",
    )
}}


select FORMAT_DATE('%m-%d',event_time) as day, count(distinct user_id) as daily_visitor
from {{ source("staging", "data") }}
group by
    day

    -- with customers as (select user_id as customer_id, from {{
    -- source('staging','data') }})
    -- select *
    -- from customers
    -- limit 100
    
