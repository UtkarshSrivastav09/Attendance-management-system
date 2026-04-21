# 🎓 SmartCampus: AI-Powered Face Recognition Attendance System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blue?style=for-the-badge)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

SmartCampus is a modernized, production-ready attendance management system that leverages Computer Vision and Machine Learning to automate attendance tracking. Featuring a sleek, Power BI-inspired dashboard, interactive analytics, and secure authentication, it represents a significant leap from traditional paper-based or legacy digital systems.

---

## 🌟 Key Features

- **🛡️ Secure Access**: Protected by an authentication gate with a professional login interface.
- **📊 Interactive Analytics**: Real-time dashboard featuring Matplotlib-powered charts showing:
  - 7-day attendance trends.
  - Today's attendance rate (Present vs. Absent).
  - Total student enrollment statistics.
- **🖼️ Advanced Face Recognition**: Uses OpenCV's LBPH (Local Binary Patterns Histograms) for high-accuracy face identification.
- **🎨 Premium UI/UX**: Dark-mode optimized interface built with CustomTkinter for a desktop-native feel.
- **📝 Automated Logging**: Generates timestamped CSV reports automatically for every subject/class.
- **🎙️ Voice Feedback**: Integrated Text-to-Speech (TTS) for user interactions and success confirmations.
- **🧪 Dummy Data Engine**: Includes a script to generate historical data for professional demonstrations.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- A working webcam

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/UtkarshSrivastav09/Attendance_Mangement_System.git
   cd Attendance_Mangement_System
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Required Folders**
   The system will automatically create necessary folders (`TrainingImage`, `Attendance`, etc.) on first run, but ensure you have the `haarcascade_frontalface_default.xml` file in the root directory.

---

## 🛠️ Usage Guide

1. **Launch the Application**
   ```bash
   python auth.py
   ```
   *The default login (if configured) will grant access to the main dashboard.*

2. **Register a New Student**
   - Navigate to **"Register Student"** in the sidebar.
   - Enter Enrollment Number and Name.
   - Click **"Take Image"**: Look at the camera; the system will capture 50 samples.
   - Click **"Train Model"**: This processes the images (LBPH) to recognize the student later.

3. **Take Attendance**
   - Click **"Take Attendance"**.
   - Select the subject/class.
   - The camera will open. Once recognized, the system will announce your name and log your attendance.

4. **View Analytics**
   - The **Dashboard** updates in real-time with charts and a "Live Feed" table of today's logs.
   - Use **"View Reports"** to browse historical CSV records.

---

## 📂 Project Structure

```text
├── Attendance/            # CSV records stored by date
├── StudentDetails/        # Master database of registered students
├── TrainingImage/         # Raw face images captured during registration
├── TrainingImageLabel/    # Trained model (Trainner.yml)
├── UI_Image/              # Assets for the GUI
├── auth.py                # Login & Security module
├── attendance.py          # Main Dashboard & Analytics
├── automaticAttedance.py  # Face recognition engine
├── generate_dummy_data.py # Demo data generator
└── requirements.txt       # Project dependencies
```

---

## 🤝 Contributing
Contributions are welcome! If you have suggestions for new features or improvements, feel free to fork the repo and create a pull request.

## ⭐ Show your support
If you find this project useful, please consider giving it a **Star** on GitHub!

---
*Developed with ❤️ by [Utkarsh Srivastav](https://github.com/UtkarshSrivastav09)*
