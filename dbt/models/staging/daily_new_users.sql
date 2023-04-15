-- Daily New User Count
select format_date('%m-%d', day) as daily, count(user_id) as daily_new_user
from (select user_id, min(event_time) as day
    from {{source("staging","data")}}
    group by user_id) as t
group by daily