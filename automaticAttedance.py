import cv2
import numpy as np
import os
import csv
import datetime
import time


def mark_attendance(enrollment, name, subject, base_dir):
    """Write a present mark for this student in today's attendance CSV."""
    ts = time.time()
    date_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
    time_str = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

    att_dir = os.path.join(base_dir, "Attendance", subject)
    os.makedirs(att_dir, exist_ok=True)
    csv_path = os.path.join(att_dir, f"{subject}_{date_str}.csv")

    # read existing so we don't duplicate
    existing = set()
    if os.path.exists(csv_path):
        with open(csv_path, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row:
                    existing.add(str(row[0]))

    if str(enrollment) not in existing:
        write_header = not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0
        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(["Enrollment", "Name", "Date", "Time"])
            writer.writerow([enrollment, name, date_str, time_str])
        return True
    return False


def TakeAttendance(subject, haarcasecade_path, trainimagelabel_path,
                   student_csv_path, base_dir, message, text_to_speech):
    """Open webcam, recognize faces, mark attendance. Press Q to stop."""

    if not os.path.exists(trainimagelabel_path):
        msg = "Trainer file not found. Please train the model first."
        text_to_speech(msg)
        message.configure(text=msg)
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainimagelabel_path)

    # build {enrollment_int: name} map from student CSV
    name_map = {}
    if os.path.exists(student_csv_path):
        with open(student_csv_path, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    try:
                        name_map[int(row[0])] = row[1]
                    except ValueError:
                        pass

    detector = cv2.CascadeClassifier(haarcasecade_path)
    if detector.empty():
        text_to_speech("Haar cascade file not found.")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        text_to_speech("Camera not accessible.")
        return

    font = cv2.FONT_HERSHEY_SIMPLEX
    marked_today = set()

    text_to_speech(f"Starting attendance for {subject}. Press Q to stop.")

    while True:
        ret, frame = cam.read()
        if not ret or frame is None:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            face_roi = gray[y:y + h, x:x + w]

            try:
                student_id, confidence = recognizer.predict(face_roi)
            except Exception:
                continue

            # confidence < 50 means good match
            if confidence < 50:
                name = name_map.get(student_id, f"ID_{student_id}")
                label = f"{name} ({int(confidence)}%)"
                color = (0, 255, 0)  # green

                if student_id not in marked_today:
                    newly = mark_attendance(student_id, name, subject, base_dir)
                    if newly:
                        marked_today.add(student_id)
                        text_to_speech(f"{name} marked present.")
            else:
                label = "Unknown"
                color = (0, 0, 255)  # red

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), font, 0.8, color, 2)

        cv2.putText(frame, f"Marked: {len(marked_today)}", (10, 30),
                    font, 0.9, (255, 255, 0), 2)
        cv2.putText(frame, "Press Q to stop", (10, 60),
                    font, 0.7, (200, 200, 200), 1)
        cv2.imshow("Attendance - " + subject, frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

    res = f"Done. {len(marked_today)} student(s) marked present for {subject}."
    message.configure(text=res)
    text_to_speech(res)
