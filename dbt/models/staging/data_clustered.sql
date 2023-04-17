{{  config(materialized='table',
    partition_by={
      "field": "event_time",
      "data_type": "TIMESTAMP",
      "granularity": "month"
    },
    cluser_by=["user_id"],
)}}


select * FROM {{source("ecommerce-behavior","data")}}