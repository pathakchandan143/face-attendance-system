import cv2
import os
import trainer   # import trainer module

def start_registration(student_id, name):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    count = 0
    dataset_path = "dataset/"
    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            cv2.imwrite(f"{dataset_path}/{student_id}.{name}.{count}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Register Face - Press ESC to exit', img)

        k = cv2.waitKey(100) & 0xff
        if k == 27:  # Press 'ESC' to exit early
            break
        elif count >= 50:  # Take 50 images
            break

    cam.release()
    cv2.destroyAllWindows()
    print(f"✅ Dataset collection done for {name} ({student_id})!")

    # 🔥 Auto-train model after dataset collection
    print("⚡ Training model, please wait...")
    trainer.train_model()
    print("✅ Training completed successfully!")
