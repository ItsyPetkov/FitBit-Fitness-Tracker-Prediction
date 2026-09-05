with minute_steps_narrow_merged_3_4 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityMinute) as activity_minute,
        Steps as steps
    from {{ source('raw', 'minuteStepsNarrow_merged_3_4') }}
),

minute_steps_narrow_merged_4_5 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityMinute) as activity_minute,
        Steps as steps
    from {{ source('raw', 'minuteStepsNarrow_merged_4_5') }}
)

select * from minute_steps_narrow_merged_3_4
union distinct
select * from minute_steps_narrow_merged_4_5