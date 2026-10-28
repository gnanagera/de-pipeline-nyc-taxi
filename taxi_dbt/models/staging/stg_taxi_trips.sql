select
    VendorID                         as vendor_id,
    tpep_pickup_datetime             as pickup_at,
    tpep_dropoff_datetime            as dropoff_at,
    cast(tpep_pickup_datetime as date) as pickup_date,
    passenger_count,
    trip_distance,
    PULocationID                     as pickup_location_id,
    DOLocationID                     as dropoff_location_id,
    payment_type,
    fare_amount,
    tip_amount,
    total_amount
from {{ source('bronze', 'taxi_trips') }}
where total_amount > 0
  and trip_distance > 0
  and tpep_dropoff_datetime > tpep_pickup_datetime
  and tpep_pickup_datetime >= '2024-01-01'
  and tpep_pickup_datetime <  '2025-01-01'
