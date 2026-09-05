import unittest

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from models.train_model import (
    train_logistic_regression,
    train_rondom_forest_classifier,
    train_support_vector_classifier,
)


class TrainModelTests(unittest.TestCase):
    def training_data(self):
        X = np.array(
            [
                [0.0, 0.0],
                [0.1, 0.2],
                [0.2, 0.1],
                [0.3, 0.3],
                [0.4, 0.2],
                [1.0, 1.0],
                [1.1, 1.2],
                [1.2, 1.1],
                [1.3, 1.3],
                [1.4, 1.2],
            ]
        )
        y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

        return X, y

    def test_training_functions_return_fitted_classifiers(self):
        X, y = self.training_data()
        training_cases = [
            (train_logistic_regression, LogisticRegression),
            (train_support_vector_classifier, SVC),
            (train_rondom_forest_classifier, RandomForestClassifier),
        ]

        for train_function, expected_type in training_cases:
            with self.subTest(train_function=train_function.__name__):
                model = train_function(X, y)

                self.assertIsInstance(model, expected_type)
                np.testing.assert_array_equal(model.classes_, np.array([0, 1]))
                self.assertEqual(model.predict(X).shape, y.shape)
                self.assertEqual(model.predict_proba(X).shape, (len(y), 2))


if __name__ == "__main__":
    unittest.main()
