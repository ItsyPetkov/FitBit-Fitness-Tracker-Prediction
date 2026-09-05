with hourly_calories as (
    select * 
    from {{ ref('stg_hourly_calories_merged_3_4_5') }}
),

hourly_intensities as (
  select * 
  from {{ ref('stg_hourly_intensities_merged_3_4_5') }}
),

hourly_steps as (
    select *
    from {{ ref('stg_hourly_steps_merged_3_4_5') }}
)

select 
  hc.user_id, 
  hc.activity_hour,
  hs.step_total as total_steps,
  hc.calories,
  hi.total_intensity,
  hi.average_intensity
from hourly_calories as hc
inner join hourly_steps as hs
  on hc.user_id = hs.user_id and hc.activity_hour = hs.activity_hour
inner join hourly_intensities as hi
  on hc.user_id = hi.user_id and hc.activity_hour = hi.activity_hour