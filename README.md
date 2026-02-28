# Face Recognition Based Attendance System

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Technical Stack](#technical-stack)
- [Face Detection: Haar Cascade Classifier](#face-detection-haar-cascade-classifier)
- [Face Recognition: LBPH Algorithm](#face-recognition-lbph-algorithm)
- [Data Collection and Dataset Structure](#data-collection-and-dataset-structure)
- [Project Structure](#project-structure)
- [Setup & Installation](#setup--installation)
- [How to Use](#how-to-use)
- [Attendance Management](#attendance-management)
- [GUI (If implemented)](#gui-if-implemented)
- [Security and Privacy Considerations](#security-and-privacy-considerations)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [References](#references)
- [License](#license)

---

## Overview

This repository implements a **Face Recognition Based Attendance System** using Python and OpenCV. The system automates attendance marking by leveraging computer vision techniques to detect and recognize faces in real time, eliminating the need for manual attendance processes. It uses Haar Cascade Classifiers for face detection and the Local Binary Patterns Histograms (LBPH) algorithm for face recognition.

---

## Features

- **Automated Face Detection** using Haar Cascades.
- **Face Recognition** with LBPH, robust to illumination and facial variation.
- **Dataset Collection**: Capture and label face images for training.
- **Attendance Logging**: Automatically records recognized faces with timestamps.
- **CSV/Excel Export**: Attendance records can be exported for further processing.
- **User-Friendly Interface**: CLI/GUI for ease of use (if implemented).
- **Real-Time Processing**: Fast and efficient recognition.
- **Modular Codebase**: Easy to extend or integrate with other systems.
- **Security Measures**: Basic data protection and privacy considerations.

---

## System Architecture

1. **Image Capture**: Users' faces are captured via webcam.
2. **Face Detection**: The system identifies faces in the frame using Haar Cascade classifiers.
3. **Data Labeling**: Each face is associated with a unique identifier (e.g., student ID).
4. **Model Training**: LBPH algorithm is trained on the collected dataset.
5. **Recognition & Attendance**: During attendance, the live feed is analyzed; recognized faces are marked as present and attendance is logged.

---

## Technical Stack

- **Programming Language**: Python (100%)
- **Key Libraries**:
  - [OpenCV](https://opencv.org/) (`cv2`): Computer vision tasks
  - [NumPy](https://numpy.org/): Numerical operations
  - [Pandas](https://pandas.pydata.org/): Data handling and exporting
  - [tkinter](https://docs.python.org/3/library/tkinter.html): GUI (if present)

---

## Face Detection: Haar Cascade Classifier

### What is Haar Cascade?

Haar Cascade is an object detection algorithm used to identify objects (in this case, faces) in an image or video. It uses the concept of "features" similar to Haar basis functions, forming a cascade of simple classifiers that efficiently scan images.

### How it Works

- **Training**: Haar features are extracted from positive and negative images.
- **Cascade**: Multiple weak classifiers are combined to form a strong classifier.
- **Detection**: The image is scanned with different window sizes to detect faces at various scales.
- **Implementation**: OpenCV provides pre-trained Haar Cascade XML files (`haarcascade_frontalface_default.xml`).

### Advantages

- Fast and lightweight.
- Good for real-time applications.

### Example Usage

```python
import cv2

# Load Haar Cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Read the image/frame
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

for (x, y, w, h) in faces:
    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
```

---

## Face Recognition: LBPH Algorithm

### What is LBPH?

LBPH (Local Binary Patterns Histograms) is a texture-based face recognition algorithm. It is particularly robust to changes in lighting and facial expressions.

### Working Principle

1. **Local Binary Pattern Calculation**:
   - For each pixel in a grayscale image, compare it with its 8 neighbors.
   - Assign 1 if the neighbor is greater or equal to the center pixel, else 0.
   - This forms an 8-bit binary number (LBP code) for the pixel.

2. **Grid Division**:
   - The image is divided into grids (e.g., 8x8).
   - Compute the histogram of LBP codes in each grid.

3. **Feature Vector**:
   - Concatenate all histograms into a single feature vector representing the face.

4. **Recognition**:
   - During recognition, the system computes the LBPH vector for the input face and compares it to the stored vectors using a distance metric (usually Euclidean).

### Advantages

- Robust to varying lighting conditions.
- Simple and fast.
- Effective with limited training data.

### Example Usage

```python
import cv2

# Initialize recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Train recognizer
recognizer.train(faces, np.array(ids))

# Save/Load trained model
recognizer.save('trainer.yml')
recognizer.read('trainer.yml')

# Predict
id_, confidence = recognizer.predict(face_roi)
```

---

## Data Collection and Dataset Structure

### Collecting Face Images

- Each user stands in front of the camera.
- The system detects the face and captures multiple samples (typically 30-100 images per user) for robustness.
- Each image is labeled with the user's ID.

### Folder Structure

```
dataset/
  ├── user1/
  │   ├── img1.jpg
  │   ├── img2.jpg
  │   └── ...
  ├── user2/
  │   ├── img1.jpg
  │   └── ...
  └── ...
```

Or, all images in one folder with filenames like `<UserID>.<sampleNumber>.jpg`.

### Label Mapping

A CSV or a dictionary maps user IDs to real names for easy lookup during attendance.

---

## Project Structure

Typical files and directories:

```
Face-Recognition-Based-Attendance-System/
├── dataset/                # Training images
├── haarcascades/           # Haar Cascade XML files
├── trainer/                # Trained LBPH models
├── attendance/             # Attendance logs
├── main.py                 # Main script
├── train.py                # Training script
├── recognize.py            # Recognition/Attendance script
├── collect_data.py         # Data collection script
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Setup & Installation

### Prerequisites

- Python 3.6+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Sample `requirements.txt`:**
```
opencv-python
numpy
pandas
```

If using GUI:
```
tk
```

### Download Haar Cascade File

Download `haarcascade_frontalface_default.xml` from [OpenCV’s GitHub](https://github.com/opencv/opencv/tree/master/data/haarcascades) and place it in the designated folder (e.g., `haarcascades/`).

---

## How to Use

### 1. Data Collection

Run the data collection script:

```bash
python collect_data.py
```
- Enter the user ID when prompted.
- The webcam will capture multiple images of the face.

### 2. Training the Model

```bash
python train.py
```
- The script will process the dataset and train the LBPH model.
- The trained model will be saved to `trainer/trainer.yml`.

### 3. Face Recognition & Attendance

```bash
python recognize.py
```
- The webcam will activate and recognize registered faces.
- Attendance will be logged in a CSV file with user ID, name, date, and time.

---

## Attendance Management

Attendance is logged in a CSV file (e.g., `attendance/attendance_YYYY-MM-DD.csv`) with columns:

- `User ID`
- `Name`
- `Date`
- `Time`
- `Status` (Present/Absent)

Sample entry:

```
1, John Doe, 2025-06-26, 08:45, Present
```

---

## GUI (If implemented)

If a GUI is implemented using `tkinter` or PyQt:

- **Login Screen:** For admin/user.
- **Data Collection:** Add new user and capture images.
- **Training:** Visual progress bar for training.
- **Attendance:** Real-time recognition and attendance marking.
- **Reports:** Export attendance to Excel/CSV.

*Refer to the `gui.py` or relevant scripts if available.*

---

## Limitations and Future Improvements

### Limitations

- Sensitive to pose and occlusion.
- Dataset quality affects recognition accuracy.
- Not robust to large-scale deployments (for enterprise, consider DNN-based models).

### Future Improvements

- Upgrade to deep learning-based face recognition (e.g., FaceNet, Dlib).
- Cloud integration for large-scale attendance.
- Mobile app for remote attendance.
- Enhanced GUI and user management.
- Real-time alerts for unrecognized faces.

---

## References

1. [OpenCV Documentation - Face Recognition](https://docs.opencv.org/master/d7/d00/tutorial_meanshift.html)
2. [LBPH Face Recognizer - OpenCV](https://docs.opencv.org/3.4/da/d60/classcv_1_1face_1_1LBPHFaceRecognizer.html)
3. [Haar Cascade Classifier - OpenCV](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)
4. [Local Binary Patterns (LBP)](https://scikit-image.org/docs/dev/auto_examples/features_detection/plot_local_binary_pattern.html)
5. [OpenCV Face Recognition GitHub Samples](https://github.com/opencv/opencv/tree/master/samples/python)

---
