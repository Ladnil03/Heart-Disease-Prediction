import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from xgboost import XGBClassifier
import joblib
import os

# -------------------------------
# STEP 1: Load Cleaned Dataset with error handling
# -------------------------------
try:
    df = pd.read_csv("../dataset/cleaned_heart.csv")
    print(f"Dataset loaded successfully. Shape: {df.shape}")
except FileNotFoundError:
    print("Error: Dataset file '../dataset/cleaned_heart.csv' not found.")
    print("Please ensure the dataset file exists in the correct path.")
    exit(1)
except Exception as e:
    print(f"Error loading dataset: {str(e)}")
    exit(1)

# Validate target column exists
if "target" not in df.columns:
    print("Error: 'target' column not found in dataset.")
    print(f"Available columns: {list(df.columns)}")
    exit(1)

X = df.drop("target", axis=1)
y = df["target"]

# -------------------------------
# STEP 2: Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------------
# STEP 3: Define XGBoost Model
# -------------------------------
xgb_model = XGBClassifier(
    n_estimators=200,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss",
    random_state=42
)

# -------------------------------
# STEP 4: Train & Evaluate
# -------------------------------
xgb_model.fit(X_train, y_train)
y_pred = xgb_model.predict(X_test)

results = {
    "Model": "XGBoost",
    "Accuracy": accuracy_score(y_test, y_pred),
    "Precision": precision_score(y_test, y_pred),
    "Recall": recall_score(y_test, y_pred),
    "F1-Score": f1_score(y_test, y_pred)
}

# -------------------------------
# STEP 5: Results
# -------------------------------
results_df = pd.DataFrame([results])

print("\nXGBoost Model Results:\n")
print(results_df.to_string(index=False))

# Step 6 : Save trained model with error handling
try:
    # Save model to backend directory
    backend_model_path = os.path.join("..", "backend", "heart_model.pkl")
    joblib.dump(xgb_model, backend_model_path)
    print(f"\nModel saved successfully to '{backend_model_path}'!")
except Exception as e:
    print(f"Error saving model: {str(e)}")
    exit(1)
