import io
import os
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

MPLCONFIGDIR = Path("/tmp") / "matplotlib"
MPLCONFIGDIR.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(MPLCONFIGDIR))

import matplotlib
import numpy as np

matplotlib.use("Agg")

from models import evaluate_model as evaluate_module
from models.evaluate_model import make_predictions


class DummyClassifier:
    def predict(self, X):
        return np.array([0, 1, 1])

    def predict_proba(self, X):
        return np.array(
            [
                [0.8, 0.2],
                [0.1, 0.9],
                [0.3, 0.7],
            ]
        )


class EvaluateModelTests(unittest.TestCase):
    def test_make_predictions_returns_predictions_and_positive_class_probabilities(self):
        predictions, probabilities = make_predictions(np.zeros((3, 2)), DummyClassifier())

        np.testing.assert_array_equal(predictions, np.array([0, 1, 1]))
        np.testing.assert_array_equal(probabilities, np.array([0.2, 0.9, 0.7]))

    def test_evaluate_model_prints_metrics_and_shows_three_plots(self):
        shown_plots = []

        with patch.object(
            evaluate_module.plt,
            "show",
            side_effect=lambda: shown_plots.append(True),
        ):
            with redirect_stdout(io.StringIO()) as output:
                evaluate_module.evaluate_model(
                    "Unit Test Model",
                    y=np.array([0, 1, 0, 1]),
                    predictions=np.array([0, 1, 1, 1]),
                    probabilities=np.array([0.1, 0.9, 0.6, 0.8]),
                )

        rendered_output = output.getvalue()

        self.assertIn("Unit Test Model", rendered_output)
        self.assertIn("Accuracy:", rendered_output)
        self.assertIn("Precision:", rendered_output)
        self.assertIn("Recall:", rendered_output)
        self.assertIn("F1 Score:", rendered_output)
        self.assertIn("Classification Report:", rendered_output)
        self.assertEqual(len(shown_plots), 3)

        evaluate_module.plt.close("all")


if __name__ == "__main__":
    unittest.main()
