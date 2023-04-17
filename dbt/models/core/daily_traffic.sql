-- Daily traffic 
{{
    config(
        materialized="table",
    )
}}
select format_date('%m-%d', event_time) as day, count(distinct user_session) as traffic
from {{ref("data_clustered")}}
group by day