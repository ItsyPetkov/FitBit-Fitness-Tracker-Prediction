with sleep_day_merged_4_5 as (
    select 
        distinct Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', SleepDay) as sleep_day,
        cast(TotalSleepRecords as string) as total_sleep_records,
        TotalMinutesAsleep as total_minutes_asleep,
        TotalTimeInBed as total_time_in_bed
    from {{ source('raw', 'sleepDay_merged_4_5')}}
)

select * from sleep_day_merged_4_5