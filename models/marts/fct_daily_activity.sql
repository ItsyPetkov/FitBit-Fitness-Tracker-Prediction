with daily_activity as (
    select *
    from {{ ref('int_daily_activity_sleep_data') }}
)

select 
    user_id,
    activity_date,
    total_steps,
    calories,
    total_distance,
    very_active_minutes,
    fairly_active_minutes,
    lightly_active_minutes,
    sedentary_minutes,
    total_minutes_asleep,
    total_time_in_bed,

    extract(dayofweek from activity_date) as day_of_week,

    format_date('%A', activity_date) as day_name,

    extract(month from activity_date) as month,

    case
        when extract(dayofweek from activity_date) in (1, 7) then 'Weekend'
        else 'Weekday'
    end as day_type
from daily_activity