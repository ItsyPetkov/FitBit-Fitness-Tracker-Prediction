with hourly_calories_merged_3_4 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityHour) as activity_hour,
        Calories as calories
    from {{ source('raw', 'hourlyCalories_merged_3_4') }}
),

hourly_calories_merged_4_5 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityHour) as activity_hour,
        Calories as calories
    from {{ source('raw', 'hourlyCalories_merged_4_5') }}
)

select * from hourly_calories_merged_3_4
union distinct
select * from hourly_calories_merged_4_5