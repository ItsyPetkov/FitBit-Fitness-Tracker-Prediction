with minute_activity as (
    select *
    from {{ ref('int_minute_activity_data') }}
)

select 
  user_id,
  cast(min(activity_minute) as date) as first_activity_date,
  cast(max(activity_minute) as date) as last_activity_date, 
  extract(day from cast(max(activity_minute) as date) - cast(min(activity_minute) as date)) as days_recorded
from minute_activity
group by user_id