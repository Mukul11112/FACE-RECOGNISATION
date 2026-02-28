import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time



# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen,text_to_speech):
    if (l1 == "") and (l2==""):
        t='Please Enter the your Enrollment Number and Name.'
        text_to_speech(t)
    elif l1=='':
        t='Please Enter the your Enrollment Number.'
        text_to_speech(t)
    elif l2 == "":
        t='Please Enter the your Name.'
        text_to_speech(t)
    else:
        try:
            cam = cv2.VideoCapture(0)
            # check camera opened
            if not cam.isOpened():
                text_to_speech("Camera not accessible. Please check camera permissions.")
                return
            detector = cv2.CascadeClassifier(haarcasecade_path)
            Enrollment = l1
            Name = l2
            sampleNum = 0
            directory = Enrollment + "_" + Name
            path = os.path.join(trainimage_path, directory)
            # create directory if missing (avoid exception if it already exists)
            os.makedirs(path, exist_ok=True)
            while True:
                ret, img = cam.read()
                if not ret or img is None:
                    # failed to read frame; notify and stop
                    text_to_speech("Failed to read from camera. Stopping capture.")
                    break
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    # build filename safely using os.path.join
                    filename = f"{Name}_{Enrollment}_{sampleNum}.jpg"
                    fullpath = os.path.join(path, filename)
                    cv2.imwrite(fullpath, gray[y : y + h, x : x + w])
                    cv2.imshow("Frame", img)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break
            cam.release()
            cv2.destroyAllWindows()
            row = [Enrollment, Name]
            # write student details using project-local StudentDetails folder
            base_dir = os.path.dirname(os.path.abspath(__file__))
            student_csv = os.path.join(base_dir, "StudentDetails", "studentdetails.csv")
            os.makedirs(os.path.dirname(student_csv), exist_ok=True)

            with open(student_csv, "a+") as csvFile:
                writer = csv.writer(csvFile, delimiter=",")
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved for ER No:" + Enrollment + " Name:" + Name
            message.configure(text=res)
            text_to_speech(res)
        except FileExistsError as F:
            F = "Student Data already exists"
            text_to_speech(F)
