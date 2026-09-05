with daily_activity as (
    select *
    from {{ ref('stg_daily_activity_merged_3_4_5') }}
),

sleed_day as (
    select *
    from {{ ref('stg_sleep_day_merged_4_5') }}
),

joined_data as (
  select 
    da.user_id,
    da.activity_date,
    da.total_steps,
    round(da.total_distance,2) as total_distance,
    round(da.tracked_distance,2) as tracked_distance,
    round(da.logged_activities_distance,2) as logged_activities_distance,
    round(da.very_active_distance,2) as very_active_distance,
    round(da.moderately_active_distance,2) as moderately_active_distance,
    round(da.light_active_distance,2) as light_active_distance,
    round(da.sedentary_active_distance,2) as sedentary_active_distance,
    da.very_active_minutes,
    da.fairly_active_minutes,
    da.lightly_active_minutes,
    da.sedentary_minutes,
    da.calories,
    sd.total_sleep_records,
    sd.total_minutes_asleep,
    sd.total_time_in_bed
  from daily_activity as da
  inner join sleed_day as sd
    on da.user_id = sd.user_id and da.activity_date = cast(sd.sleep_day as date)
),

detect_duplicates as (
  select *, 
    row_number() over(partition by user_id, activity_date) as rn
  from joined_data
)

select 
  user_id,
  activity_date,
  total_steps,
  total_distance,
  tracked_distance,
  logged_activities_distance,
  very_active_distance,
  moderately_active_distance,
  light_active_distance,
  sedentary_active_distance,
  very_active_minutes,
  fairly_active_minutes,
  lightly_active_minutes,
  sedentary_minutes,
  calories,
  total_sleep_records,
  total_minutes_asleep,
  total_time_in_bed 
from detect_duplicates
where rn = 1
