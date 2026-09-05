with hourly_intensities_merged_3_4 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityHour) as activity_hour,
        TotalIntensity as total_intensity,
        round(AverageIntensity,2) as average_intensity
    from {{ source('raw', 'hourlyIntensities_merged_3_4') }}
),

hourly_intensities_merged_4_5 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', ActivityHour) as activity_hour,
        TotalIntensity as total_intensity,
        round(AverageIntensity,2) as average_intensity
    from {{ source('raw', 'hourlyIntensities_merged_4_5') }}
)

select * from hourly_intensities_merged_3_4
union distinct
select * from hourly_intensities_merged_4_5