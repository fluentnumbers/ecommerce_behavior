-- Top 10 products with High Product Affinity(which products are purchased at the same time)
select t1.product_id as first_pid, t2.product_id as second_pid, count(1) as cnt
from
    (
        select user_session, product_id
        from {{ source("staging", "data") }}
        where event_type = 'purchase'
        group by user_session, product_id
    ) as t1

inner join
    (
        select user_session, product_id
        from {{ source("staging", "data") }}
        where event_type = 'purchase'
        group by user_session, product_id
    ) as t2

    on t1.user_session = t2.user_session
    and t1.product_id <> t2.product_id
    and t1.product_id > t2.product_id

group by first_pid, second_pid
order by cnt desc
limit 10
