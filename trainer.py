import cv2
import os
import numpy as np
import csv

# Make sure path is SAME everywhere
dataset_path = "dataset"
recognizer = cv2.face.LBPHFaceRecognizer_create()

id_name_map = {}

def train_model():
    faces, ids = [], []
    for file in os.listdir(dataset_path):
        path = os.path.join(dataset_path, file)

        # Only process images
        if not file.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue  # skip unreadable files

        parts = file.split(".")
        if len(parts) < 3:  # safety check
            continue

        try:
            id = int(parts[0])
            name = parts[1]
        except ValueError:
            continue

        faces.append(img)
        ids.append(id)
        id_name_map[id] = name

    if len(faces) < 2:
        print("❌ Not enough training data! Please register at least one student (50 images).")
        return

    recognizer.train(faces, np.array(ids))
    recognizer.save("trainer.yml")

    # Save ID–Name mapping
    with open("id_name_map.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name"])
        for k, v in id_name_map.items():
            writer.writerow([k, v])

    print("✅ Training complete! Model saved as trainer.yml and mapping saved in id_name_map.csv")


if __name__ == "__main__":
    train_model()
