import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from features.build_features import build_features
from models.train_model import (
    train_logistic_regression, 
    train_random_forest_classifier, 
    train_support_vector_classifier)
from models.evaluate_model import make_predictions, evaluate_model
from utils import setup_logging

def main():

    logger = logging.getLogger(__name__)
    logger.info("Starting model training pipeline")

    # =====================================
    # 1. LOAD INITIAL DATASET
    # =====================================

    logger.info("Loading dataset from ./dataset/ml_dataset.csv")

    df = pd.read_csv('./dataset/ml_dataset.csv')

    logger.info("Loaded dataset with %s rows and %s columns", df.shape[0], df.shape[1])

    # Separating the response variable (y) from the set of predictor variables (X)
    X = df.iloc[:, 0:-1]
    y = df.iloc[:, -1]

    logger.info("Split dataset into predictors and response variable")

    # =====================================
    # 2. PERFORM FEATURE SELECTION
    # =====================================

    # List of relevant features according to feature importance
    relevant_features = ['steps_per_hour', 'calories_per_hour', 'total_intensities_per_hour', 'average_intensities_per_hour',
                     'hour_of_day', 'day_of_week', 'steps_per_minute', 'calories_per_minute', 'total_steps_per_day', 
                     'total_calories_per_day', 'days_recorded']

    X = X[relevant_features]

    logger.info("Selected %s relevant features", len(relevant_features))

    # =====================================
    # 3. PERFORM FEATURE ENGINEERING
    # =====================================

    logger.info("Building engineered features")

    X = build_features(X)

    logger.info("Feature engineering complete; predictor dataset now has %s columns", X.shape[1])

    # =====================================
    # 4. PERFORM TRAIN-TEST SPLIT 70/30%
    # =====================================

    logger.info("Splitting data into train and test sets")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.30, random_state=42, stratify=y
    )

    logger.info("Created train set with %s rows and test set with %s rows", X_train.shape[0], X_test.shape[0])

    # =====================================
    # 5. SCALE DATA
    # =====================================

    logger.info("Scaling numeric predictors")
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    logger.info("Scaling complete")

    # =====================================
    # 6. MODEL INSTATIATION AND TRAINING
    # =====================================

    logger.info("Training logistic regression model")
    logistic_model = train_logistic_regression(X_train_scaled, y_train)

    logger.info("Training support vector classifier model")
    svc_model = train_support_vector_classifier(X_train_scaled, y_train)

    logger.info("Training random forest classifier model")
    rf_model = train_random_forest_classifier(X_train, y_train)

    logger.info("Model training complete")

    # =====================================
    # 7. MODEL PREDICTIONS 
    # =====================================

    logger.info("Generating model predictions")

    logistic_model_predictions, logistic_model_probabilities = make_predictions(X_test_scaled, logistic_model)
    svc_model_predictions, svc_model_probabilites = make_predictions(X_test_scaled, svc_model)
    rf_model_predictions, rf_models_probabilites = make_predictions(X_test, rf_model)

    logger.info("Prediction generation complete")

    # =====================================
    # 8. MODEL EVALUATION
    # =====================================

    logger.info("Evaluating logistic regression model")
    evaluate_model("Initial Logistic Regression", y_test, logistic_model_predictions, logistic_model_probabilities)

    logger.info("Evaluating support vector classifier model")
    evaluate_model("Initial Support Vector Classifier", y_test, svc_model_predictions, svc_model_probabilites)

    logger.info("Evaluating random forest classifier model")
    evaluate_model("Initial Random Forest Classifier", y_test, rf_model_predictions, rf_models_probabilites)

    logger.info("Model training pipeline complete")

if __name__ == "__main__":
    setup_logging()

    try:
        main()
    except Exception:
        logging.getLogger(__name__).exception("Model training pipeline failed")
        raise
