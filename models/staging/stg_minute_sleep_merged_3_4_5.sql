with minute_sleep_merged_3_4 as (
    select 
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', date) as recorded_activity_date,
        cast(value as string) as sleep_type,
        logId as log_id
    from {{ source('raw', 'minuteSleep_merged_3_4') }}
),

minute_sleep_merged_4_5 as (
    select  
        Id as user_id,
        safe.parse_datetime('%m/%d/%Y %I:%M:%S %p', date) as recorded_activity_date,
        cast(value as string) as sleep_type,
        logId as log_id
    from {{ source('raw', 'minuteSleep_merged_4_5') }}
)

select * from minute_sleep_merged_3_4
union distinct
select * from minute_sleep_merged_4_5