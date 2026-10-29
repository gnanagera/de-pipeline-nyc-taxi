select
    trip_id,
    pickup_date,
    pickup_location_id,
    dropoff_location_id,
    coalesce(payment_type_id, 5)                          as payment_type_id,
    vendor_id,
    pickup_at,
    dropoff_at,
    passenger_count,
    trip_distance,
    round(timestampdiff(SECOND, pickup_at, dropoff_at) / 60.0, 2) as trip_duration_minutes,
    fare_amount,
    tip_amount,
    tolls_amount,
    total_amount,
    case when fare_amount > 0
         then round(tip_amount / fare_amount, 4) end      as tip_pct
from {{ ref('stg_taxi_trips') }}
