import unittest

import pandas as pd

from features.build_features import build_features


class BuildFeaturesTests(unittest.TestCase):
    def test_build_features_adds_expected_engineered_columns(self):
        df = pd.DataFrame(
            {
                "steps_per_hour": [10, 0],
                "calories_per_hour": [2, 5],
                "steps_per_minute": [2, 0],
                "calories_per_minute": [1, 3],
                "total_steps_per_day": [50, 0],
                "total_calories_per_day": [100, 25],
            }
        )

        result = build_features(df)

        self.assertIs(result, df)
        self.assertEqual(result["hourly_steps_calories"].tolist(), [20, 0])
        self.assertEqual(result["minute_steps_calories"].tolist(), [2, 0])
        self.assertAlmostEqual(result["calories_per_step_hour"].iloc[0], 2 / 11)
        self.assertAlmostEqual(result["calories_per_step_hour"].iloc[1], 5)
        self.assertAlmostEqual(result["calories_per_step_minute"].iloc[0], 1 / 3)
        self.assertAlmostEqual(result["calories_per_step_minute"].iloc[1], 3)
        self.assertAlmostEqual(result["daily_calories_per_step"].iloc[0], 100 / 51)
        self.assertAlmostEqual(result["daily_calories_per_step"].iloc[1], 25)


if __name__ == "__main__":
    unittest.main()
