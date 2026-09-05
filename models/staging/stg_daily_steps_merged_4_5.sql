with daily_steps_merged_4_5 as (
    select  
        Id as user_id,
        safe.parse_date('%m/%d/%Y', ActivityDay) as activity_day,
        StepTotal as step_total
    from {{ source('raw', 'dailySteps_merged_4_5')}}
)

select * from daily_steps_merged_4_5