"""
Phase 2 Logistic Regression Template
Project: Flight Delay Prediction

This script mirrors the Phase 2 workflow:
- Load team sample files
- Clean valid year and label rows
- Encode categorical variables
- Train Logistic Regression
- Evaluate accuracy, precision, and confusion matrix
- Save model results
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, confusion_matrix, classification_report

# Replace these paths with your actual sample files.
files = {
    "hritik": "data/hritik_sample_2008.csv",
    "takudzwa": "data/takudzwa_sample_2004.csv",
    "alex": "data/alex_sample_1997.csv",
    "surakshya": "data/surakshya_sample_1995.csv",
}

# Load available files.
dataframes = []
for name, path in files.items():
    try:
        df = pd.read_csv(path)
        df["Source"] = name
        dataframes.append(df)
    except FileNotFoundError:
        print(f"Skipping missing file: {path}")

if not dataframes:
    raise FileNotFoundError("No sample files found. Add CSV files to the data folder.")

raw_df = pd.concat(dataframes, ignore_index=True)

# Clean valid years and target labels.
clean_df = raw_df[raw_df["Year"].isin([1995, 1997, 2004, 2008, "1995", "1997", "2004", "2008"])]
clean_df = clean_df[clean_df["Delayed"].isin(["Y", "N"])].reset_index(drop=True)
clean_df.to_csv("data/team_combined_sample_final.csv", index=False)

# Target encoding.
y = clean_df["Delayed"].map({"N": 0, "Y": 1})

# Drop target and high-cardinality columns.
X = clean_df.drop(columns=["Delayed"], errors="ignore")
X = X.drop(columns=["TailNum", "FlightNum", "Source"], errors="ignore")

# Fill missing values and one-hot encode.
X = X.fillna("Unknown")
X_encoded = pd.get_dummies(X, drop_first=True)

# Optional sample reduction used to avoid kernel crashes.
if len(X_encoded) > 20000:
    X_encoded = X_encoded.sample(n=20000, random_state=42)
    y = y.loc[X_encoded.index]

X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

model = LogisticRegression(max_iter=300, solver="liblinear", random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Confusion Matrix:")
print(cm)
print("Classification Report:")
print(classification_report(y_test, y_pred))

results_df = pd.DataFrame([
    {
        "Model": "Logistic Regression",
        "Accuracy": accuracy,
        "Precision": precision,
        "Confusion_Matrix": cm.tolist(),
        "Test_Split": "20%",
    }
])

results_df.to_csv("data/hritik_logistic_regression_results.csv", index=False)
