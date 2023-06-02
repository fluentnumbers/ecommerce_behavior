{{
    config(
        materialized="table",
    )
}}

with
    daily_customers as (
        select
            -- PARSE_DATE("%y-%m-%d",format_date("%y-%m-%d", event_time)) as day,
            CAST(event_time as date) as day,
            count(distinct user_id) as daily_visitor
        from {{ ref("data_clustered") }}
        group by day
    )
select *
from daily_customers
