from datetime import datetime, UTC
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

alerts = [
    {
        "timestamp": datetime.now(UTC),
        "src_ip": "192.168.12.150",
        "dst_ip": "192.168.12.233",
        "prediction": "attack",
        "attack_type": "syn_flood",
        "confidence": 99.8,
    },
    {
        "timestamp": datetime.now(UTC),
        "src_ip": "192.168.12.150",
        "dst_ip": "192.168.12.233",
        "prediction": "attack",
        "attack_type": "nmap_scan",
        "confidence": 93.4,
    },
    {
        "timestamp": datetime.now(UTC),
        "src_ip": "192.168.12.150",
        "dst_ip": "192.168.12.233",
        "prediction": "attack",
        "attack_type": "service_scan",
        "confidence": 88.7,
    },
    {
        "timestamp": datetime.now(UTC),
        "src_ip": "192.168.12.150",
        "dst_ip": "192.168.12.233",
        "prediction": "benign",
        "attack_type": "benign_mixed_realistic",
        "confidence": 91.2,
    },
]

for alert in alerts:
    db.collection("alerts").add(alert)

print("Uploaded multiple SOC alerts to Firestore.")