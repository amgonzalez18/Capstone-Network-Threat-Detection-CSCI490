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

# =========================
# LOAD + CLEAN DATA
# =========================
df = pd.read_csv("pcaps/zeek_test_output/final_datasets/combined_dataset.csv")

# Remove any accidental repeated header rows inside the combined CSV
df = df[df["ts"] != "ts"].copy()

# Replace "-" with NaN
df.replace("-", np.nan, inplace=True)

numeric_cols = ["duration", "orig_pkts", "resp_pkts"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_cols] = df[numeric_cols].fillna(0)

# Fill remaining categorical/string missing values
df = df.fillna("missing")

# Save original cleaned columns for reporting
df_original = df.copy()

# Drop columns that can leak labels or create memorization
df = df.drop(columns=[
    "uid",
    "src_ip",
    "dst_ip",
    "src_port",
    "dst_port",
    "ts",
    "service",
    "conn_state",
    "orig_bytes",
    "resp_bytes",
])

# One-hot encode categorical network fields
df = pd.get_dummies(df, columns=["proto"])

# =========================
# MODEL 1: BENIGN VS ATTACK
# =========================
binary_df = df.copy()

binary_label_encoder = LabelEncoder()
binary_df["label"] = binary_label_encoder.fit_transform(binary_df["label"])

print("\nBinary label mapping:")
for i, name in enumerate(binary_label_encoder.classes_):
    print(f"{i} = {name}")

X_binary = binary_df.drop(columns=["label", "attack_type"])
y_binary = binary_df["label"]

Xb_train, Xb_test, yb_train, yb_test = train_test_split(
    X_binary,
    y_binary,
    test_size=0.2,
    random_state=42,
    stratify=y_binary
)

binary_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features="sqrt",
    random_state=42,
    class_weight="balanced"
)
binary_model.fit(Xb_train, yb_train)

yb_pred = binary_model.predict(Xb_test)

attack_index = list(binary_label_encoder.classes_).index("attack")
yb_probs = binary_model.predict_proba(Xb_test)[:, attack_index]

print("\n==============================")
print("MODEL 1: BENIGN VS ATTACK")
print("==============================")
print(classification_report(
    yb_test,
    yb_pred,
    target_names=binary_label_encoder.classes_
))

cm_binary = confusion_matrix(yb_test, yb_pred)
disp_binary = ConfusionMatrixDisplay(
    confusion_matrix=cm_binary,
    display_labels=binary_label_encoder.classes_
)
disp_binary.plot()
plt.title("Model 1 Confusion Matrix: Benign vs Attack")
plt.show()

fpr, tpr, _ = roc_curve(yb_test, yb_probs, pos_label=attack_index)
roc_auc = auc(fpr, tpr)

plt.figure()
plt.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}")
plt.plot([0, 1], [0, 1], linestyle="--")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("Model 1 ROC Curve: Attack Detection")
plt.legend()
plt.show()

binary_counts = df_original["label"].value_counts()

plt.figure()
plt.pie(binary_counts, labels=binary_counts.index, autopct="%1.1f%%")
plt.title("Binary Class Distribution")
plt.show()

# =========================
# MODEL 2: ATTACK TYPE
# only train on attack rows
# =========================
attack_df = df[df_original["label"] == "attack"].copy()

attack_type_encoder = LabelEncoder()
attack_df["attack_type"] = attack_type_encoder.fit_transform(attack_df["attack_type"])

print("\nAttack type mapping:")
for i, name in enumerate(attack_type_encoder.classes_):
    print(f"{i} = {name}")

X_attack = attack_df.drop(columns=["label", "attack_type"])
y_attack = attack_df["attack_type"]

Xa_train, Xa_test, ya_train, ya_test = train_test_split(
    X_attack,
    y_attack,
    test_size=0.2,
    random_state=42,
    stratify=y_attack
)

attack_model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    min_samples_split=10,
    min_samples_leaf=4,
    max_features="sqrt",
    random_state=42,
    class_weight="balanced"
)
attack_model.fit(Xa_train, ya_train)

ya_pred = attack_model.predict(Xa_test)

print("\n==============================")
print("MODEL 2: ATTACK TYPE")
print("==============================")
print(classification_report(
    ya_test,
    ya_pred,
    target_names=attack_type_encoder.classes_
))

cm_attack = confusion_matrix(ya_test, ya_pred)
disp_attack = ConfusionMatrixDisplay(
    confusion_matrix=cm_attack,
    display_labels=attack_type_encoder.classes_
)
disp_attack.plot(xticks_rotation=45)
plt.title("Model 2 Confusion Matrix: Attack Type")
plt.show()

attack_counts = df_original[df_original["label"] == "attack"]["attack_type"].value_counts()

plt.figure()
plt.pie(attack_counts, labels=attack_counts.index, autopct="%1.1f%%")
plt.title("Attack Type Distribution")
plt.show()

# =========================
# PRACTICAL PIPELINE DEMO
# this simulates how the system behaves as one IDS
# =========================
print("\n==============================")
print("PIPELINE DEMO")
print("==============================")

sample_index = Xb_test.index[0]
sample_features = X_binary.loc[[sample_index]]

binary_prediction = binary_model.predict(sample_features)[0]
binary_prediction_name = binary_label_encoder.inverse_transform([binary_prediction])[0]

print(f"Stage 1 prediction: {binary_prediction_name}")

if binary_prediction_name == "attack":
    sample_attack_features = sample_features.reindex(columns=X_attack.columns, fill_value=0)
    attack_prediction = attack_model.predict(sample_attack_features)[0]
    attack_prediction_name = attack_type_encoder.inverse_transform([attack_prediction])[0]
    print(f"Stage 2 prediction: {attack_prediction_name}")
else:
    print("Stage 2 skipped because traffic is benign.")