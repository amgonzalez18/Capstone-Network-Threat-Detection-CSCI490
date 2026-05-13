import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_curve,
    auc,
    ConfusionMatrixDisplay
)
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv("pcaps/zeek_test_output/final_datasets/combined_dataset.csv")

# Remove any accidental repeated header rows inside the combined CSV
df = df[df["ts"] != "ts"].copy()

# Fix missing values represented as "-"
df.replace("-", np.nan, inplace=True)

# Convert numeric columns
numeric_cols = ["duration", "orig_bytes", "resp_bytes", "orig_pkts", "resp_pkts"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Fill numeric missing values with 0
df[numeric_cols] = df[numeric_cols].fillna(0)

# Fill remaining categorical/string missing values
df = df.fillna("missing")

# Drop columns that can leak labels or create memorization
df = df.drop(columns=[
    "uid",
    "src_ip",
    "dst_ip",
    "src_port",
    "dst_port",
    "ts",
    "service"
])

# Encode categorical features
df = pd.get_dummies(df, columns=["proto", "conn_state"])

# Encode labels
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["label"])

print("\nLabel mapping:")
for i, name in enumerate(label_encoder.classes_):
    print(f"{i} = {name}")

# Features / labels
X = df.drop(columns=["label", "attack_type"])
y = df["label"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features="sqrt",
    random_state=42,
    class_weight="balanced"
)
model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print("\n=== Classification Report ===")
print(classification_report(
    y_test,
    y_pred,
    target_names=label_encoder.classes_
))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=label_encoder.classes_
)
disp.plot()
plt.title("Confusion Matrix: Benign vs Attack")
plt.show()

# ROC Curve
attack_index = list(label_encoder.classes_).index("attack")
y_probs = model.predict_proba(X_test)[:, attack_index]

fpr, tpr, _ = roc_curve(y_test, y_probs, pos_label=attack_index)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.title(f"ROC Curve: Attack Detection (AUC = {roc_auc:.2f})")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.show()

# Pie Chart
counts = df["label"].value_counts().sort_index()
label_names = label_encoder.inverse_transform(counts.index)

plt.figure()
plt.pie(counts, labels=label_names, autopct="%1.1f%%")
plt.title("Dataset Distribution")
plt.show()