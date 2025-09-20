import cv2
import datetime
import csv
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
haar_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

attendance_file = "attendance.csv"

# Create attendance file if not exists
if not os.path.isfile(attendance_file):
    with open(attendance_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Date", "Time"])

def load_id_name_map():
    mapping = {}
    if os.path.isfile("id_name_map.csv"):
        with open("id_name_map.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mapping[int(row["ID"])] = row["Name"]
    return mapping

def recognize():
    recognizer.read("trainer.yml")
    cap = cv2.VideoCapture(0)

    names = load_id_name_map()
    marked = set()

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = haar_cascade.detectMultiScale( gray,
                                scaleFactor=1.1,
                                minNeighbors=7,
                                minSize=(100, 100) )

        for (x,y,w,h) in faces:
            id_, conf = recognizer.predict(gray[y:y+h, x:x+w])

            if conf < 55:
                name = names.get(id_, f"ID {id_}")
                color = (0, 255, 0)

                if id_ not in marked:
                    now = datetime.datetime.now()
                    with open(attendance_file, "a", newline="") as f:
                        writer = csv.writer(f)
                        writer.writerow([id_, name, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")])
                    marked.add(id_)
                    print(f"✅ Attendance marked: {id_} - {name}")
            else:
                name = "Unknown"
                color = (0, 0, 255)

            cv2.rectangle(frame,(x,y),(x+w,y+h),color,2)
            cv2.putText(frame,name,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)

        cv2.imshow("Face Recognition - Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize()
