with daily_activity_merged_3_4 as (
    select 
        Id as user_id, 
        safe.parse_date('%m/%d/%Y', ActivityDate) as activity_date,
        TotalSteps as total_steps,
        TotalDistance as total_distance,
        TrackedDistance as tracked_distance,
        LoggedActivitiesDistance as logged_activities_distance,
        VeryActiveDistance as very_active_distance,
        ModeratelyActiveDistance as moderately_active_distance,
        LightActiveDistance as light_active_distance,
        SedentaryActiveDistance as sedentary_active_distance,
        VeryActiveMinutes as very_active_minutes,
        FairlyActiveDistance as fairly_active_minutes,
        LightlyActiveDistance as lightly_active_minutes,
        SedentaryMinutes as sedentary_minutes,
        Calories as calories
    from {{ source('raw', 'dailyActivity_merged_3_4') }}
),

daily_activity_merged_4_5 as (
    select 
        Id as user_id, 
        safe.parse_date('%m/%d/%Y', ActivityDate) as activity_date,
        TotalSteps as total_steps,
        TotalDistance as total_distance,
        TrackerDistance as tracked_distance,
        LoggedActivitiesDistance as logged_activities_distance,
        VeryActiveDistance as very_active_distance,
        ModeratelyActiveDistance as moderately_active_distance,
        LightActiveDistance as light_active_distance,
        SedentaryActiveDistance as sedentary_active_distance,
        VeryActiveMinutes as very_active_minutes,
        FairlyActiveMinutes as fairly_active_minutes,
        LightlyActiveMinutes as lightly_active_minutes,
        SedentaryMinutes as sedentary_minutes,
        Calories as calories
    from {{ source('raw', 'dailyActivity_merged_4_5') }}
)

select * from daily_activity_merged_3_4
union distinct
select * from daily_activity_merged_4_5