-- Bounce Rate
{{
    config(
        materialized="table",
    )
}}
select format_date('%m-%d', event_time) as day, count(user_session) as cnt
from
    (
        select
            user_session,
            event_time,
            event_type,
            lead(event_time) over (
                partition by user_session order by event_time
            ) as after_event_time
        from {{ source("staging", "data") }}
    ) as t
where after_event_time is null
group by day
