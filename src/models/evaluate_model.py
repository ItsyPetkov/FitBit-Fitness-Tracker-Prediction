import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score
)

def make_predictions(X, model):

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    return predictions, probabilities

def evaluate_model(name, y, predictions, probabilities):

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print("Accuracy:", accuracy_score(y, predictions))
    print("Precision:", precision_score(y, predictions))
    print("Recall:", recall_score(y, predictions))
    print("F1 Score:", f1_score(y, predictions))

    print("\nClassification Report:\n")
    print(classification_report(y, predictions))


    # =====================================
    # CONFUSION MATRIX
    # =====================================

    cm = confusion_matrix(y, predictions)

    ConfusionMatrixDisplay(
        confusion_matrix=cm
    ).plot()

    plt.title(f"{name} - Confusion Matrix")
    plt.show()


    # =====================================
    # ROC CURVE
    # =====================================

    fpr, tpr, thresholds = roc_curve(
        y, probabilities
    )

    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(7, 5))

    plt.plot(
        fpr,
        tpr,
        label=f"AUC = {roc_auc:.3f}"
    )

    plt.plot(
        [0, 1],
        [0, 1],
        linestyle='--'
    )

    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(f"{name} - ROC Curve")
    plt.legend()

    plt.show()


    # =====================================
    # PRECISION-RECALL CURVE
    # =====================================

    precision, recall, thresholds = precision_recall_curve(
        y, probabilities
    )

    average_precision = average_precision_score(
        y, probabilities
    )

    plt.figure(figsize=(7, 5))

    plt.plot(
        recall,
        precision,
        label=f"AP = {average_precision:.3f}"
    )

    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(f"{name} - Precision-Recall Curve")
    plt.legend()

    plt.show()