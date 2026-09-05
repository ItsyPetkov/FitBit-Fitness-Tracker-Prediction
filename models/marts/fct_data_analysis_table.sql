with hourly_activity as (
    select *
    from {{ ref('fct_hourly_activity') }}
),

minute_activity as (
    select *
    from {{ ref('fct_minute_activity') }}
),

daily_activity as (
    select * 
    from {{ ref('fct_daily_activity') }}
),

dim_users as (
    select *
    from {{ ref('fct_dim_users') }}
)

select
  ha.user_id,
  ha.activity_hour,
  ha.total_steps as steps_per_hour,
  ha.calories as calories_per_hour,
  ha.total_intensity as total_intensities_per_hour,
  ha.average_intensity as average_intensities_per_hour,
  ha.hour_of_day,
  ha.day_of_week,
  ma.day_name,
  case
    when extract(dayofweek from ha.activity_hour) in (1, 7) then 'Weekend'
    else 'Weekday'
  end as day_type,
  ha.time_of_day,
  cast(ha.activity_hour as date) as activity_date,
  extract(month from ha.activity_hour) as month,
  ma.activity_minute,
  ma.steps as steps_per_minute,
  ma.calories as calories_per_minute,
  ma.intensity as intensity_type,
  da.total_steps as total_steps_per_day,
  da.calories as total_calories_per_day,
  da.total_distance as total_distance_per_day,
  da.very_active_minutes,
  da.fairly_active_minutes,
  da.lightly_active_minutes,
  da.sedentary_minutes,
  da.total_minutes_asleep,
  da.total_time_in_bed,
  du.first_activity_date,
  du.last_activity_date,
  du.days_recorded
from hourly_activity as ha
inner join minute_activity as ma
  on ha.user_id = ma.user_id and ma.activity_minute = ha.activity_hour
inner join daily_activity as da
  on ha.user_id = da.user_id
inner join dim_users as du
  on ha.user_id = du.user_id