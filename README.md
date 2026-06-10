# 🚦 Red Light Violation Detection System

## 📖 Introduction

Traffic signal violations are one of the major causes of road accidents and congestion. This project presents an AI-powered Red Light Violation Detection System that automatically identifies vehicles crossing a stop line during a red traffic signal.

Using YOLOv8 and OpenCV, the system analyzes traffic footage, detects vehicles in real time, tracks their movement, and records violations with supporting evidence.

---

## 🎯 Problem Statement

Manual traffic monitoring is time-consuming, error-prone, and difficult to scale.

The objective of this project is to automate the detection of red-light violations by:

* Detecting vehicles from traffic footage
* Monitoring signal status
* Identifying vehicles crossing the stop line during a red signal
* Generating violation records automatically

---

## ✨ Key Features

✅ Real-Time Vehicle Detection

✅ Red Light Violation Identification

✅ Automated Violation Logging

✅ Vehicle Evidence Capture

✅ Annotated Video Generation

✅ Computer Vision-Based Monitoring

✅ Customizable Traffic Rules

---

## 🛠️ Tech Stack

| Technology       | Purpose                          |
| ---------------- | -------------------------------- |
| Python           | Core Development                 |
| OpenCV           | Image & Video Processing         |
| YOLOv8           | Vehicle Detection                |
| NumPy            | Numerical Operations             |
| Jupyter Notebook | Model Training & Experimentation |

---

## ⚙️ System Workflow

```text
Traffic Video
      │
      ▼
Vehicle Detection (YOLOv8)
      │
      ▼
Traffic Signal Monitoring
      │
      ▼
Violation Detection Logic
      │
      ▼
Evidence Capture & Logging
      │
      ▼
Annotated Output Video
```

---

## 📂 Project Structure

```text
Red-Light-Violation-Detection-System
│
├── main.py
├── Vehicle_Detection_Training.ipynb
├── violations.csv
├── README.md
```

---

## 🚀 How It Works

1. Input traffic footage is processed frame-by-frame.
2. YOLOv8 detects vehicles present in each frame.
3. The system continuously checks traffic signal status.
4. Vehicles crossing the stop line during a red signal are flagged.
5. Violation details are recorded automatically.
6. Evidence and statistics are generated for further analysis.

---

## 📊 Output

* Vehicle Detection Results
* Violation Logs
* Evidence Images
* Annotated Video Output
* Traffic Monitoring Statistics

---

## 🌍 Real-World Applications

* Smart Cities
* Intelligent Traffic Management
* Automated Law Enforcement
* Road Safety Systems
* Urban Transportation Analytics

---

## 🔮 Future Enhancements

* Automatic Number Plate Recognition (ANPR)
* Real-Time CCTV Integration
* Web Dashboard for Monitoring
* Cloud-Based Storage
* Multi-Camera Traffic Analysis
* Advanced Vehicle Tracking

---

## 👨‍💻 Author

### T. Shirisha

B.E. Artificial Intelligence & Data Science

Chaitanya Bharathi Institute of Technology (CBIT)


