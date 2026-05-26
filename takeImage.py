import csv
import os
import cv2
import numpy as np
import pandas as pd
import datetime
import time


def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    # ── input validation ──────────────────────────────────────────
    if l1 == "" and l2 == "":
        text_to_speech("Please enter your Enrollment Number and Name.")
        return
    if l1 == "":
        text_to_speech("Please enter your Enrollment Number.")
        return
    if l2 == "":
        text_to_speech("Please enter your Name.")
        return

    try:
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            text_to_speech("Camera not accessible. Please check camera permissions.")
            return

        detector = cv2.CascadeClassifier(haarcasecade_path)
        if detector.empty():
            text_to_speech("Haar cascade file not found. Check the path.")
            cam.release()
            return

        Enrollment = l1.strip()
        Name = l2.strip()
        sampleNum = 0

        # folder = Enrollment_Name so trainImage can extract ID from folder name
        directory = Enrollment + "_" + Name
        path = os.path.join(trainimage_path, directory)
        os.makedirs(path, exist_ok=True)

        while True:
            ret, img = cam.read()
            if not ret or img is None:
                text_to_speech("Failed to read from camera.")
                break

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                sampleNum += 1
                filename = f"{Name}_{Enrollment}_{sampleNum}.jpg"
                fullpath = os.path.join(path, filename)
                cv2.imwrite(fullpath, gray[y:y + h, x:x + w])

            cv2.imshow("Capturing Faces - Press Q to stop", img)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            if sampleNum >= 50:
                break

        cam.release()
        cv2.destroyAllWindows()

        if sampleNum == 0:
            msg = "No face detected. Please try again with better lighting."
            text_to_speech(msg)
            message.configure(text=msg)
            return

        # ── save student details to CSV ───────────────────────────
        base_dir = os.path.dirname(os.path.abspath(__file__))
        student_csv = os.path.join(base_dir, "StudentDetails", "studentdetails.csv")
        os.makedirs(os.path.dirname(student_csv), exist_ok=True)

        write_header = not os.path.exists(student_csv) or os.path.getsize(student_csv) == 0
        with open(student_csv, "a+", newline="") as csvFile:
            writer = csv.writer(csvFile)
            if write_header:
                writer.writerow(["Enrollment", "Name"])
            writer.writerow([Enrollment, Name])

        res = f"Images Saved for Enrollment: {Enrollment}  Name: {Name}"
        message.configure(text=res)
        text_to_speech(res)

    except Exception as e:
        msg = f"Error during image capture: {str(e)}"
        text_to_speech(msg)
        message.configure(text=msg)
