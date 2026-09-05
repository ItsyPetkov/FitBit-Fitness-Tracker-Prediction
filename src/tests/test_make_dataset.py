import importlib.util
import io
import sys
import types
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import pandas as pd


def load_make_dataset_module():
    fake_bigquery = types.ModuleType("google.cloud.bigquery")
    fake_bigquery.Client = lambda: None

    fake_cloud = types.ModuleType("google.cloud")
    fake_cloud.bigquery = fake_bigquery

    fake_google = types.ModuleType("google")
    fake_google.cloud = fake_cloud

    fake_modules = {
        "google": fake_google,
        "google.cloud": fake_cloud,
        "google.cloud.bigquery": fake_bigquery,
    }

    module_path = Path(__file__).resolve().parents[1] / "dataset" / "make_dataset.py"
    spec = importlib.util.spec_from_file_location("make_dataset_for_test", module_path)
    module = importlib.util.module_from_spec(spec)

    with patch.dict(sys.modules, fake_modules):
        spec.loader.exec_module(module)

    return module


def configure_fake_bigquery(module, source_df):
    saved_csvs = {}
    clients = []

    class FakeQueryJob:
        def to_dataframe(self):
            return source_df.copy()

    class FakeClient:
        def __init__(self):
            self.query_text = None
            clients.append(self)

        def query(self, query):
            self.query_text = query
            return FakeQueryJob()

    def fake_to_csv(self, path, index=False):
        saved_csvs[str(path)] = {
            "data": self.copy(),
            "index": index,
        }

    return FakeClient, fake_to_csv, saved_csvs, clients


class MakeDatasetTests(unittest.TestCase):
    def test_construct_dataset_saves_raw_bigquery_data(self):
        source_df = pd.DataFrame(
            {
                "intensity_type": ["0", "1", "2"],
                "steps": [100, 200, 300],
            }
        )
        module = load_make_dataset_module()
        fake_client, fake_to_csv, saved_csvs, clients = configure_fake_bigquery(
            module,
            source_df,
        )

        with patch.object(module.bigquery, "Client", fake_client):
            with patch.object(pd.DataFrame, "to_csv", fake_to_csv):
                with redirect_stdout(io.StringIO()):
                    module.construct_dataset(raw=True)

        self.assertIn("../data_raw/data.csv", saved_csvs)
        self.assertFalse(saved_csvs["../data_raw/data.csv"]["index"])
        pd.testing.assert_frame_equal(saved_csvs["../data_raw/data.csv"]["data"], source_df)
        self.assertIn("fct_data_analysis_table", clients[0].query_text)

    def test_construct_dataset_creates_binary_high_intensity_target(self):
        source_df = pd.DataFrame(
            {
                "intensity_type": ["0", "1", "2", "3"],
                "steps": [100, 200, 300, 400],
            }
        )
        module = load_make_dataset_module()
        fake_client, fake_to_csv, saved_csvs, _ = configure_fake_bigquery(
            module,
            source_df,
        )

        with patch.object(module.bigquery, "Client", fake_client):
            with patch.object(pd.DataFrame, "to_csv", fake_to_csv):
                with redirect_stdout(io.StringIO()):
                    module.construct_dataset(raw=False)

        saved_df = saved_csvs["ml_dataset.csv"]["data"]
        self.assertFalse(saved_csvs["ml_dataset.csv"]["index"])
        self.assertEqual(saved_df["high_intensity"].tolist(), [0, 0, 1, 1])


if __name__ == "__main__":
    unittest.main()
