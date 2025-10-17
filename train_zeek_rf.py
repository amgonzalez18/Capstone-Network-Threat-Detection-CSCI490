
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.utils.class_weight import compute_class_weight
import joblib

df = pd.read_csv("conn.csv") 

num_cols_raw = ["duration","orig_bytes","resp_bytes","missed_bytes",
                "orig_pkts","orig_ip_bytes","resp_pkts","resp_ip_bytes"]
for c in num_cols_raw:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c], errors="coerce")

df[num_cols_raw] = df[num_cols_raw].fillna(0)

df["bytes_total"] = df["orig_bytes"] + df["resp_bytes"]
df["bytes_ratio"] = (df["orig_bytes"] + 1) / (df["resp_bytes"] + 1)
df["pkts_total"]  = df["orig_pkts"] + df["resp_pkts"]
df["pkts_ratio"]  = (df["orig_pkts"] + 1) / (df["resp_pkts"] + 1)
df["is_tcp"] = (df.get("proto","").astype(str) == "tcp").astype(int)
df["is_udp"] = (df.get("proto","").astype(str) == "udp").astype(int)
df["hist_len"] = df.get("history","").astype(str).map(lambda x: len(x) if isinstance(x,str) else 0)

if df["label"].dtype == "O":
    df["label"] = df["label"].str.lower().map({"malicious":1,"benign":0})
y = df["label"].astype(int)

num_cols = [c for c in ["duration","orig_bytes","resp_bytes","missed_bytes",
                        "orig_pkts","orig_ip_bytes","resp_pkts","resp_ip_bytes",
                        "bytes_total","bytes_ratio","pkts_total","pkts_ratio","hist_len","is_tcp","is_udp"]
            if c in df.columns]

cat_cols = [c for c in ["proto","service","conn_state","local_orig","local_resp"]
            if c in df.columns]

X = df[num_cols + cat_cols]

classes = np.array([0,1])
weights = compute_class_weight(class_weight="balanced", classes=classes, y=y)
class_weight = {int(k):float(v) for k,v in zip(classes, weights)}

pre = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
    ],
    remainder="drop",
)

rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=None,
    min_samples_leaf=2,
    n_jobs=-1,
    class_weight=class_weight,
    random_state=42,
)

clf = Pipeline(steps=[("pre", pre), ("rf", rf)])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:,1]
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred, digits=4))
try:
    print("ROC-AUC:", roc_auc_score(y_test, y_prob))
except Exception:
    pass
joblib.dump(clf, "zeek_rf_pipeline.joblib")
print("Saved model → zeek_rf_pipeline.joblib")
