from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

def train_logistic_regression(X, y):

    logistic_model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    logistic_model.fit(X, y)

    return logistic_model

def train_support_vector_classifier(X, y):

    svm_model = SVC(
        kernel='rbf',
        probability=True,
        random_state=42
    )

    svm_model.fit(X, y)

    return svm_model

def train_random_forest_classifier(X, y):

    rf_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )

    rf_model.fit(X, y)

    return rf_model

