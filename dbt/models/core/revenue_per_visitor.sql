-- Revenue per Visitor

select t1.day as day, daily_visitor, sum_of_revenue, round(sum_of_revenue/daily_visitor,2) as rpv
from (
    select format_date('%m-%d', event_time) as day, count(distinct user_id) as daily_visitor
    from {{ref("data_clustered")}}
    group by day) as t1

inner join (
    select format_date('%m-%d', event_time) as day, sum(price) as sum_of_revenue
    from {{ref("data_clustered")}}
    group by day) as t2
    
    on t1.day=t2.day

order by t1.day asc