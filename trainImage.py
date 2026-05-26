import os
import cv2
import numpy as np
from PIL import Image


def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    faces, ids = getImagesAndLabels(trainimage_path)

    if len(faces) == 0:
        res = "No training images found. Please capture images first."
        message.configure(text=res)
        text_to_speech(res)
        return

    recognizer.train(faces, np.array(ids))

    os.makedirs(os.path.dirname(trainimagelabel_path), exist_ok=True)
    recognizer.save(trainimagelabel_path)

    res = f"Model trained on {len(set(ids))} student(s), {len(faces)} images."
    message.configure(text=res)
    text_to_speech(res)


def getImagesAndLabels(path):
    faces = []
    ids = []

    if not os.path.exists(path):
        return faces, ids

    for folder_name in os.listdir(path):
        folder_path = os.path.join(path, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # folder name format: Enrollment_Name
        parts = folder_name.split("_")
        try:
            student_id = int(parts[0])
        except ValueError:
            print(f"Skipping folder (cannot parse ID): {folder_name}")
            continue

        for img_file in os.listdir(folder_path):
            if not img_file.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            img_path = os.path.join(folder_path, img_file)
            try:
                pil_img = Image.open(img_path).convert("L")
                img_np = np.array(pil_img, dtype="uint8")
                faces.append(img_np)
                ids.append(student_id)
            except Exception as e:
                print(f"Skipping {img_path}: {e}")
                continue

    return faces, ids
