with hourly_steps_merged_3_4 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityHour) as activity_hour,
        StepTotal as step_total
    from {{ source('raw', 'hourlySteps_merged_3_4')}}
),

hourly_steps_merged_4_5 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityHour) as activity_hour,
        StepTotal as step_total
    from {{ source('raw', 'hourlySteps_merged_4_5')}}
)

select * from hourly_steps_merged_3_4
union distinct
select * from hourly_steps_merged_4_5