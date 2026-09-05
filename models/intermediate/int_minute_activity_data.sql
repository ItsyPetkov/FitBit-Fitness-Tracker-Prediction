with minute_calories as (
    select * 
    from {{ ref('stg_minute_calories_narrow_merged_3_4_5') }}
),

minute_intensities as (
    select *
    from {{ ref('stg_minute_intensities_narrow_merged_3_4_5') }}
),

minute_mets as (
    select *
    from {{ ref('stg_minute_mets_narrow_merged_3_4_5') }}
),

minute_steps as (
    select *
    from {{ ref('stg_minute_steps_narrow_merged_3_4_5') }}
)

select  
    distinct mc.user_id, 
    mc.activity_minute,
    ms.steps,
    round(mc.calories,2) as calories,
    mm.mets,
    mi.intensity
from minute_calories as mc
inner join minute_intensities as mi 
  on mc.user_id = mi.user_id and mc.activity_minute = mi.activity_minute
inner join minute_mets as mm
  on mc.user_id = mm.user_id and mc.activity_minute = mm.activity_minute
inner join minute_steps as ms
  on mc.user_id = ms.user_id and mc.activity_minute = ms.activity_minute