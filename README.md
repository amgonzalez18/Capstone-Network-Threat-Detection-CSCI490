# Capstone-Network-Threat-Detection-CSCI490
This is my senior project where I am building a home lab that simulates network traffic and attacks and then applies a machine learning model that will be an intrusion detection pipeline to detect threats in a network system. The detections will be visualized in a Flutter Firebase dashboard app.


---

# Repository Organization

```text
main
├── pcaps/
├── pcaps/zeek_test_output/
├── pcaps/zeek_test_output/final_datasets/
├── final_model.py
├── train_model.py
├── run_model_upload_alerts.py
├── upload_predictions_to_firestore.py
├── soc_dashboard_flutter/
└── README.md
```

## Folder and File Descriptions

### `pcaps/`

Contains the packet capture (`.pcap`) files generated from the isolated home lab environment. These captures include both benign traffic and simulated cyberattacks such as:

* SYN Flood
* Nmap scans
* UDP scans
* SSH brute force attempts
* Benign SSH/web browsing/ping traffic

⚠️ Warning: Some packet capture files are large and may take time to download or open in Wireshark.

---

### `pcaps/zeek_test_output/`

Contains all Zeek-generated feature extraction folders created from the packet captures. Each folder stores processed network logs and extracted connection features for a specific traffic scenario.

Example:

```text
phase3_nmap_service_scan_Features/
phase4_dos_synflood_Features/
```

These folders contain:

* `conn.log`
* `conn_labeled.csv`
* Zeek-generated network metadata

---

### `pcaps/zeek_test_output/final_datasets/`

Contains the final labeled CSV datasets used for machine learning model training and evaluation.

Important dataset:

```text
combined_dataset.csv
```

This dataset combines all benign and attack traffic into a single labeled dataset used by the final intrusion detection pipeline.

---

### `final_model.py`

Main machine learning intrusion detection pipeline used in the final project.

This script:

* Loads the combined dataset
* Performs preprocessing
* Runs binary classification:

  * benign vs attack
* Runs attack-type classification:

  * SYN flood
  * Nmap scan
  * UDP scan
  * brute force
  * service scan
* Displays classification metrics and predictions

The script loads the dataset from:

```text
pcaps/zeek_test_output/final_datasets/combined_dataset.csv
```

To run:

```bash
python final_model.py
```

---

### `train_model.py`

Training pipeline used during model development and experimentation.

This script was used to:

* Train the machine learning models
* Evaluate model performance
* Generate classification reports

---

### `upload_predictions_to_firestore.py`

Uploads generated prediction alerts into Firebase Firestore.

This script creates SOC alert entries including:

* source IP
* destination IP
* prediction type
* attack type
* confidence score
* timestamp

---

### `run_model_upload_alerts.py`

Runs the final ML pipeline and uploads generated alerts directly into Firestore for visualization on the SOC dashboard.

This is the main script used for the live dashboard demonstration.

To run:

```bash
python run_model_upload_alerts.py
```

---

### `soc_dashboard_flutter/`

Flutter Firebase SOC dashboard application.

The dashboard:

* Retrieves alerts from Firebase Firestore
* Displays attack and benign traffic
* Shows confidence scores
* Displays recent alerts in real time
* Tracks attack statistics

The dashboard is built using:

* Flutter
* Firebase Firestore
* Android Studio emulator

---

# Running the Project

## Running the Machine Learning Pipeline

Open the repository root in VS Code.

Run:

```bash
python final_model.py
```

or

```bash
python run_model_upload_alerts.py
```

---

## Running the Flutter SOC Dashboard

1. Open the `soc_dashboard_flutter/` folder in Android Studio or VS Code
2. Start an Android emulator
3. Run:

```bash
flutter pub get
flutter run
```

The dashboard will retrieve alerts from Firebase Firestore in real time.

---

# Home Lab Network Setup

The project used a physically isolated network lab environment consisting of:

* Raspberry Pi victim device
* Raspberry Pi network sensor
* Kali Linux attacker VM
* Netgear managed switch with port mirroring

## Static IP Configuration

Static IPs were assigned to:

* Kali Linux VM
* Raspberry Pi sensor
* Raspberry Pi victim

Example IP structure:

```text
192.168.12.x
```

---

## Kali Linux Configuration

Kali Linux was configured using:

* VMware bridged networking
* USB Ethernet adapter
* Static IP configuration

Additional networking fixes were performed within Kali network settings to ensure proper communication with the isolated lab environment.

---

## Port Mirroring Configuration

Port mirroring was enabled through the Netgear switch GUI.

This allowed:

* Raspberry Pi sensor to capture mirrored traffic
* Zeek to analyze live network traffic
* Packet captures to be recorded for ML processing

Typical workflow:

```text
Network Traffic
    ↓
Port Mirroring
    ↓
Zeek Feature Extraction
    ↓
Machine Learning Pipeline
    ↓
Firebase Firestore
    ↓
Flutter SOC Dashboard
```



<img width="845" height="1232" alt="Lab" src="https://github.com/user-attachments/assets/5fb75913-d6ea-406a-a3d8-f6b2430b80f1" />
