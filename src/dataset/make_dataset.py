from google.cloud import bigquery
import pandas as pd

def construct_dataset(raw=True):
    client = bigquery.Client()

    query = """
    SELECT *
    FROM `tonal-mote-500309-c6.analytics.fct_data_analysis_table`
    """

    df = client.query(query).to_dataframe()

    print(df.head())

    if raw:
        df.to_csv('../data_raw/data.csv', index=False)
    else:
        df["high_intensity"] = df["intensity_type"].apply(lambda x: 0 if x in ["0", "1"] else 1)
        df.to_csv('ml_dataset.csv', index=False)

if __name__ == "__main__":
    construct_dataset()
    construct_dataset(False)