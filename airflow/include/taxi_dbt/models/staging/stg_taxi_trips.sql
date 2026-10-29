with source as (
    select * from {{ source('bronze', 'taxi_trips') }}
),

cleaned as (
    select
        md5(concat_ws('|',
            cast(VendorID as string),
            cast(tpep_pickup_datetime as string),
            cast(tpep_dropoff_datetime as string),
            cast(PULocationID as string),
            cast(DOLocationID as string),
            cast(total_amount as string)
        ))                                   as trip_id,
        VendorID                             as vendor_id,
        tpep_pickup_datetime                 as pickup_at,
        tpep_dropoff_datetime                as dropoff_at,
        cast(tpep_pickup_datetime as date)   as pickup_date,
        passenger_count,
        trip_distance,
        RatecodeID                           as rate_code_id,
        PULocationID                         as pickup_location_id,
        DOLocationID                         as dropoff_location_id,
        payment_type                         as payment_type_id,
        fare_amount,
        tip_amount,
        tolls_amount,
        total_amount
    from source
    where total_amount > 0
      and trip_distance > 0
      and tpep_dropoff_datetime > tpep_pickup_datetime
      and tpep_pickup_datetime >= '2024-01-01'
      and tpep_pickup_datetime <  '2025-01-01'
)

select * from cleaned
qualify row_number() over (partition by trip_id order by pickup_at) = 1
