# Face Recognition Attendance — Starter Kit

This is a minimal, step-by-step starter project to build a **Face Recognition Attendance System**.

## Project Structure
```
face_attendance_starter/
├── README.md
├── requirements.txt
├── camera_test.py
├── register_student.py
├── attendance_cam.py
└── data/
    ├── images/         # Optional: store reference photos (if not capturing via webcam)
    ├── logs/           # Attendance CSV files by date
    └── encodings.pickle (auto-created after registering first student)
```

## 0) Prerequisites
- **Python 3.10 or 3.11 (64-bit)** installed and added to PATH.
- A **webcam** (built-in or USB).
- Good lighting in the classroom.

### Windows build tools (only if `face_recognition` fails to install):
- Install **Desktop development with C++** using Visual Studio Build Tools.
- Install **CMake** (optional).

If installation is difficult on your machine, you can temporarily use `opencv-contrib-python`
with LBPH as a fallback (lower accuracy).

## 1) Create a virtual environment & install dependencies
```bash
# From this folder
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

> If `face_recognition` fails: try `pip install cmake dlib` first, then `pip install face-recognition`.
> As a fallback (lower accuracy): `pip install opencv-contrib-python` and ask for the LBPH script alternative.

## 2) Test your camera
```bash
python camera_test.py
```
- A window should open showing your webcam. Press **q** to quit.

## 3) Register students (create face embeddings)
```bash
python register_student.py --student_id S001 --name "Alice Kumar"
```
- Look straight into the camera; the script will capture multiple frames.
- After success, it will update/create `data/encodings.pickle`.
- Repeat the command for each student.

> Alternatively, if you have photos, place them in `data/images/S001/` and run:
```bash
python register_student.py --student_id S001 --name "Alice Kumar" --from_images
```

## 4) Start attendance (real-time recognition)
```bash
python attendance_cam.py --session "Math-101" --tolerance 0.5
```
- When your face is recognized, your name will appear, and attendance will be marked **once per session**.
- A CSV file will be created at `data/logs/YYYY-MM-DD.csv`.
- Press **q** to stop.

## 5) Next steps (later)
- Add a Flask/FastAPI backend and a simple dashboard for reports.
- Move from CSV to **SQLite/MySQL/MongoDB**.
- Add **liveness detection** and **anti-spoofing**.
- Deploy on a mini PC (e.g., Raspberry Pi 4) or a classroom laptop.

---

**Privacy note:** Get explicit consent from students; store data securely; purge encodings for students who leave.
