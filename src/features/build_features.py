import pandas as pd

def build_features_with_path(path):

    df = pd.read_csv(path)

    df['hourly_steps_calories'] = df['steps_per_hour'] * df['calories_per_hour']
    df['minute_steps_calories'] = df['steps_per_minute'] * df['calories_per_minute']
    df['calories_per_step_hour'] = df['calories_per_hour'] / (df['steps_per_hour'] + 1)
    df['calories_per_step_minute'] = df['calories_per_minute'] / (df['steps_per_minute'] + 1)
    df['daily_calories_per_step'] = df['total_calories_per_day'] / (df['total_steps_per_day'] + 1)

    print(df.head())

def build_features(df):

    df['hourly_steps_calories'] = df['steps_per_hour'] * df['calories_per_hour']
    df['minute_steps_calories'] = df['steps_per_minute'] * df['calories_per_minute']
    df['calories_per_step_hour'] = df['calories_per_hour'] / (df['steps_per_hour'] + 1)
    df['calories_per_step_minute'] = df['calories_per_minute'] / (df['steps_per_minute'] + 1)
    df['daily_calories_per_step'] = df['total_calories_per_day'] / (df['total_steps_per_day'] + 1)

    return df

if __name__ == "__main__":
    build_features_with_path('../data_raw/data.csv')