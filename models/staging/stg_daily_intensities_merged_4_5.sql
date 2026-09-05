with daily_intensities_merged_4_5 as (
    select 
        Id as user_id,
        safe.parse_date('%m/%d/%Y', ActivityDay) as activity_day,
        SedentaryMinutes as sedentary_minutes,
        LightlyActiveMinutes as lightly_active_minutes,
        FairlyActiveMinutes as fairly_active_minutes,
        VeryActiveMinutes as very_active_minutes,
        SedentaryActiveDistance as sedentary_active_distance,
        LightActiveDistance as light_active_distance,
        ModeratelyActiveDistance as moderately_active_distance,
        VeryActiveDistance as very_active_distance
    from {{ source('raw', 'dailyIntensities_merged_4_5') }}
)

select * from daily_intensities_merged_4_5