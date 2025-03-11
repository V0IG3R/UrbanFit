# UrbanFit - AI-Powered Exercise Tracking 🏋️‍♂️🤖  

UrbanFit is an AI-powered exercise tracking application that uses **MediaPipe Pose Detection** to analyze workouts in real time.  
It provides **live feedback, rep counting, and posture analysis** while displaying a **skeletal overlay on the video feed**.  
Below the video, **rep counter, stage status, and posture feedback** are shown in **separate boxes** for a clean and intuitive user experience.  

-------------------------------------------------------------------------------

## 🚀 Features  

📹 **Real-time pose detection** using MediaPipe  
🔢 **Automated rep counting** for various exercises  
🏋️ **Posture feedback** to ensure correct form  
📊 **Live statistics display** below the video  
🌐 **Frontend (React) & Backend (FastAPI) integration**  
🛠 **Modular design** for adding new exercises  

-------------------------------------------------------------------------------

## 📁 Folder Structure  

```
project/
├── backend/               # Backend API (FastAPI)
│   ├── bicep_curls.py     # Bicep curls logic
│   ├── deadlifts.py       # Deadlifts logic
│   ├── lunges.py          # Lunges logic
│   ├── pushups.py         # Pushups logic
│   ├── situps.py          # Situps logic
│   ├── squats.py          # Squats logic
│   ├── state.py           # Stores real-time exercise state
│   └── main.py            # API entry point (FastAPI)
│
├── exercises/             # Calibration data for each exercise
│   ├── bicep_curls/
│   │   ├── calibration/
│   │   │   └── bicep_curl_calibration.txt
│   │   └── videos/        # Legacy videos (not used)
│   ├── deadlifts/
│   │   ├── calibration/
│   │   │   └── deadlift_angles.txt
│   │   └── videos/
│   ├── lunges/
│   │   ├── calibration/
│   │   │   └── lunge_calibration.txt
│   │   └── videos/
│   ├── pushups/
│   │   ├── calibration/
│   │   │   └── pushup_calibration.txt
│   │   └── videos/
│   ├── situps/
│   │   ├── calibration/
│   │   │   └── situp_calibration.txt
│   │   └── videos/
│   └── squats/
│       ├── calibration/
│       │   └── squat_calibration.txt
│       └── videos/
│
├── frontend/              # Frontend (React)
│   ├── public/
│   │   └── index.html     # Main HTML file
│   └── src/
│       ├── components/
│       │   └── ExercisePage.js  # Main exercise tracking page
│       ├── styles/
│       │   └── ExercisePage.css # Styling for UI
│
└── README.md              # Project documentation
```

-------------------------------------------------------------------------------

## 🛠 Installation  

### **1️⃣ Clone the Repository**  
```bash
git clone https://github.com/yourusername/urbanfit.git
cd urbanfit
```

### **2️⃣ Setup Virtual Environment (Recommended)**
It is recommended to use a **virtual environment** for the backend to avoid dependency conflicts.

#### **For Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### **For macOS/Linux:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **3️⃣ Install Frontend Dependencies (React)**
```bash
cd frontend
npm install
```

-------------------------------------------------------------------------------

## 🚀 Usage  

### **Run Backend Server (FastAPI)**
```bash
cd backend
source venv/bin/activate  # Activate the virtual environment (Linux/macOS)
# On Windows, use: venv\Scripts\activate

uvicorn main:app --reload
```
- The backend will start at **http://localhost:8000**.

### **Run Frontend (React)**
```bash
cd frontend
npm start
```
- The React app will open at **http://localhost:3000**.

-------------------------------------------------------------------------------

## 🎯 How It Works  

1️⃣ **Frontend captures video feed** and extracts **pose landmarks** using MediaPipe.  
2️⃣ Only **landmark data** (not full video frames) is sent to the backend.  
3️⃣ The backend processes **rep counting, posture analysis, and stage tracking**.  
4️⃣ The **skeletal overlay is displayed on the video**, while rep stats are shown **below the video**.  

-------------------------------------------------------------------------------

## 📌 Supported Exercises  

✅ **Bicep Curls**  
✅ **Deadlifts**  
✅ **Lunges**  
✅ **Pushups**  
✅ **Situps**  
✅ **Squats**  

Each exercise has its **own calibration file** stored under the `exercises/` directory.

-------------------------------------------------------------------------------

## 🤖 Tech Stack  

- **Frontend:** React, JavaScript, MediaPipe Pose API  
- **Backend:** FastAPI, Python, OpenCV, NumPy  
- **Data Processing:** JSON-based calibration files  

-------------------------------------------------------------------------------

## 📜 License  

This project is **open-source** and available under the **MIT License**.

-------------------------------------------------------------------------------

## 💡 Future Improvements  

📌 **Add new exercises dynamically**  
🎨 **Improve UI/UX** with advanced overlays  
📊 **More detailed analytics** for form improvement  

-------------------------------------------------------------------------------

## 👨‍💻 Author  

Developed by **Debarun Joardar** 🚀  
For inquiries, contact **djoardar2001@gmail.com**  
