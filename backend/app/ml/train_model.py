import os
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report

from app.ml.dataset_generator import generate_synthetic_dataset


MODEL_PATH = "saved_models/fatigue_model.joblib"


def train_fatigue_model():
    df = generate_synthetic_dataset(num_samples=1000)

    feature_columns = [
        "avg_hrv",
        "avg_rhr",
        "avg_cbt",
        "avg_glucose",
        "glucose_std",
        "max_glucose",
        "sleep_log_count",
        "meal_log_count"
    ]

    X = df[feature_columns]
    y = df["fatigue_risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    train_accuracy = accuracy_score(y_train, train_predictions)
    test_accuracy = accuracy_score(y_test, test_predictions)

    cv_scores = cross_val_score(model, X, y, cv=5)

    feature_importance = dict(
        zip(
            feature_columns,
            [round(float(v), 4) for v in model.feature_importances_]
        )
    )

    report = classification_report(
        y_test,
        test_predictions,
        output_dict=True,
        zero_division=0
    )

    os.makedirs("saved_models", exist_ok=True)

    model_bundle = {
        "model": model,
        "feature_columns": feature_columns,
        "evaluation": {
            "training_samples": len(df),
            "train_accuracy": round(train_accuracy, 4),
            "test_accuracy": round(test_accuracy, 4),
            "cross_validation_accuracy_mean": round(float(cv_scores.mean()), 4),
            "cross_validation_accuracy_std": round(float(cv_scores.std()), 4),
            "feature_importance": feature_importance,
            "classification_report": report,
            "data_warning": (
                "This model is trained on synthetic rule-generated labels. "
                "It validates the ML pipeline, not clinical performance."
            )
        }
    }

    joblib.dump(model_bundle, MODEL_PATH)

    return model_bundle


def load_or_train_fatigue_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)

    return train_fatigue_model()