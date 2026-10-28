select
    z.Borough                    as borough,
    z.Zone                       as zone,
    count(*)                     as trips,
    round(sum(t.total_amount), 2) as revenue
from {{ ref('stg_taxi_trips') }} t
left join {{ ref('taxi_zone_lookup') }} z
    on t.pickup_location_id = z.LocationID
group by 1, 2
