-- Number of unique customer visited our shop by day
{{
    config(
        materialized="table",
    )
}}
select CAST(event_time as date) as day, count(distinct user_id) as daily_visitor
from {{ ref("data_clustered") }}
group by day
