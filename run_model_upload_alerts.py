import pandas as pd
import numpy as np
import firebase_admin

from datetime import datetime, UTC
from firebase_admin import credentials, firestore

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# =========================
# FIREBASE SETUP
# =========================
cred = credentials.Certificate("firebase_key.json")

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("pcaps/zeek_test_output/final_datasets/combined_dataset.csv")
df = df[df["ts"] != "ts"].copy()

df.replace("-", np.nan, inplace=True)

numeric_cols = ["duration", "orig_bytes", "resp_bytes", "orig_pkts", "resp_pkts"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df[numeric_cols] = df[numeric_cols].fillna(0)
df = df.fillna("missing")

# Save original fields for dashboard display
df_original = df.copy()

# Drop label-leaking or identifier columns
df = df.drop(columns=[
    "uid",
    "src_ip",
    "dst_ip",
    "src_port",
    "dst_port",
    "ts",
    "service",
    "conn_state"
])

# Encode proto only
df = pd.get_dummies(df, columns=["proto"])

# =========================
# MODEL 1: BENIGN VS ATTACK
# =========================
binary_df = df.copy()

binary_encoder = LabelEncoder()
binary_df["label"] = binary_encoder.fit_transform(binary_df["label"])

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

# =========================
# MODEL 2: ATTACK TYPE
# =========================
attack_df = df[df_original["label"] == "attack"].copy()

attack_encoder = LabelEncoder()
attack_df["attack_type"] = attack_encoder.fit_transform(attack_df["attack_type"])

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

# =========================
# UPLOAD REAL MODEL PREDICTIONS
# =========================
print("Uploading model predictions to Firestore...")

sample_rows = Xb_test.head(10)

for index, row in sample_rows.iterrows():
    row_df = row.to_frame().T

    binary_pred = binary_model.predict(row_df)[0]
    binary_name = binary_encoder.inverse_transform([binary_pred])[0]

    binary_probs = binary_model.predict_proba(row_df)[0]
    binary_confidence = round(float(max(binary_probs) * 100), 2)

    if binary_name == "attack":
        attack_row = row_df.reindex(columns=X_attack.columns, fill_value=0)

        attack_pred = attack_model.predict(attack_row)[0]
        attack_name = attack_encoder.inverse_transform([attack_pred])[0]

        attack_probs = attack_model.predict_proba(attack_row)[0]
        confidence = round(float(max(attack_probs) * 100), 2)
    else:
        attack_name = df_original.loc[index, "attack_type"]
        confidence = binary_confidence

    alert = {
        "timestamp": datetime.now(UTC),
        "src_ip": str(df_original.loc[index, "src_ip"]),
        "dst_ip": str(df_original.loc[index, "dst_ip"]),
        "prediction": str(binary_name),
        "attack_type": str(attack_name),
        "confidence": confidence,
    }

    db.collection("alerts").add(alert)

print("Uploaded 10 model-generated alerts to Firestore.")