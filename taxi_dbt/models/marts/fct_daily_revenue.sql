select
    pickup_date,
    count(*)                       as trips,
    round(sum(total_amount), 2)    as revenue,
    round(avg(trip_distance), 2)   as avg_distance,
    round(avg(tip_amount), 2)      as avg_tip
from {{ ref('stg_taxi_trips') }}
group by pickup_date
