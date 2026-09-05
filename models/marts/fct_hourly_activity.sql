with hourly_activity as (

    select *
    from {{ ref('int_hourly_activity_data') }}

)

select
    user_id,
    activity_hour,

    total_steps,
    calories,

    total_intensity,
    average_intensity,

    extract(hour from activity_hour) as hour_of_day,
    extract(dayofweek from activity_hour) as day_of_week,

    case
        when extract(hour from activity_hour) between 6 and 11 then 'Morning'
        when extract(hour from activity_hour) between 12 and 17 then 'Afternoon'
        when extract(hour from activity_hour) between 18 and 21 then 'Evening'
        else 'Night'
    end as time_of_day

from hourly_activity