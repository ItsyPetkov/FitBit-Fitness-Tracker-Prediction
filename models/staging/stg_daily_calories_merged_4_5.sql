with daily_calories_merged_4_5 as (
    select 
        Id as user_id,
        safe.parse_date('%m/%d/%Y', ActivityDay) as activity_day,
        Calories as calories
    from {{ source('raw', 'dailyCalories_merged_4_5') }}
)

select * from daily_calories_merged_4_5
