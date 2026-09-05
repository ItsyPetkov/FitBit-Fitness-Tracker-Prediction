with minute_activity as (
    select *
    from {{ ref('int_minute_activity_data') }}
)

select 
    user_id,
    activity_minute,
    steps,
    calories,
    intensity,

    extract(hour from activity_minute) as hour_of_day,

    extract(dayofweek from activity_minute) as day_of_week,

    format_datetime('%A', activity_minute) as day_name,

    case
        when extract(hour from activity_minute) between 6 and 11 then 'Morning'
        when extract(hour from activity_minute) between 12 and 17 then 'Afternoon'
        when extract(hour from activity_minute) between 18 and 21 then 'Evening'
        else 'Night'
    end as time_of_day
from minute_activity