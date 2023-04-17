-- Which event occured most before purchase
{{
    config(
        materialized="table",
    )
}}

select before_event, count(after_event) as cnt
from
    (
        select
            event_type as before_event,
            lead(event_type, 1) over (
                partition by user_id order by event_time
            ) as after_event
        from {{ source("staging", "data") }}
    ) as t
where after_event = 'purchase'
group by before_event
order by cnt desc
