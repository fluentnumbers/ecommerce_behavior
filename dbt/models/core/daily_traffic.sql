-- Daily traffic 
{{
    config(
        materialized="table",
    )
}}
select CAST(event_time as date) as day, count(distinct user_session) as traffic
from {{ref("data_clustered")}}
group by day