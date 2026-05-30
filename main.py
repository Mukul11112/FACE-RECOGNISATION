import tkinter as tk
from tkinter import *
import os
import pyttsx3
# ── paths ─────────────────────────────────────────────────────────
BASE_DIR         = os.path.dirname(os.path.abspath(__file__))
HAAR_PATH        = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
TRAIN_IMG_PATH   = os.path.join(BASE_DIR, "TrainingImage")
TRAINER_PATH     = os.path.join(BASE_DIR, "TrainingImageLabel", "trainer.yml")
STUDENT_CSV_PATH = os.path.join(BASE_DIR, "StudentDetails", "studentdetails.csv")

# create required folders on first run
for folder in [TRAIN_IMG_PATH,
               os.path.join(BASE_DIR, "TrainingImageLabel"),
               os.path.join(BASE_DIR, "StudentDetails"),
               os.path.join(BASE_DIR, "Attendance")]:
    os.makedirs(folder, exist_ok=True)

# ── text-to-speech ────────────────────────────────────────────────
engine = pyttsx3.init()
def text_to_speech(text):
    print("[TTS]", text)
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def err_screen(msg):
    text_to_speech(msg)

# ── button actions (lazy imports so a bad file doesn't crash startup)
def do_capture():
    from takeImage import TakeImage
    TakeImage(enroll_entry.get(), name_entry.get(),
              HAAR_PATH, TRAIN_IMG_PATH,
              msg_label, err_screen, text_to_speech)

def do_train():
    from trainImage import TrainImage
    TrainImage(HAAR_PATH, TRAIN_IMG_PATH,
               TRAINER_PATH, msg_label, text_to_speech)

def do_auto_attendance():
    sub = subject_entry.get().strip()
    if sub == "":
        text_to_speech("Please enter the subject name.")
        msg_label.configure(text="Enter subject name first.")
        return
    from automaticAttendance import TakeAttendance
    TakeAttendance(sub, HAAR_PATH, TRAINER_PATH,
                   STUDENT_CSV_PATH, BASE_DIR,
                   msg_label, text_to_speech)

def do_manual_attendance():
    from takemanually import manually_fill
    manually_fill()

def do_view_attendance():
    from show_attendance import subjectchoose
    subjectchoose(text_to_speech)

# ── main window ───────────────────────────────────────────────────
window = tk.Tk()
window.title("Face Recognition Attendance System")
window.geometry("900x580")
window.configure(background="lightblue")
window.resizable(False, False)

tk.Label(window,
         text="Face Recognition Attendance System",
         bg="black", fg="green",
         font=("arial", 22, "bold")).pack(pady=18)

tk.Label(window, bg="black", relief=RIDGE, bd=4, height=1).pack(fill=X, padx=20)

# ── input fields ──────────────────────────────────────────────────
inp = tk.Frame(window, bg="black")
inp.pack(pady=14)

lbl_cfg = dict(bg="black", fg="white", font=("times", 14))
ent_cfg = dict(width=22, bd=4, bg="black", fg="yellow", relief=RIDGE, font=("times", 14, "bold"))

tk.Label(inp, text="Enrollment No :", **lbl_cfg).grid(row=0, column=0, padx=10, pady=6, sticky="e")
enroll_entry = tk.Entry(inp, **ent_cfg)
enroll_entry.grid(row=0, column=1, pady=6)

tk.Label(inp, text="Name :", **lbl_cfg).grid(row=1, column=0, padx=10, pady=6, sticky="e")
name_entry = tk.Entry(inp, **ent_cfg)
name_entry.grid(row=1, column=1, pady=6)

tk.Label(inp, text="Subject :", **lbl_cfg).grid(row=2, column=0, padx=10, pady=6, sticky="e")
subject_entry = tk.Entry(inp, **ent_cfg)
subject_entry.grid(row=2, column=1, pady=6)

# ── status label ──────────────────────────────────────────────────
msg_label = tk.Label(window, text="", bg="black", fg="cyan",
                     font=("times", 12), wraplength=860)
msg_label.pack(pady=4)

# ── buttons ───────────────────────────────────────────────────────
btn_frame = tk.Frame(window, bg="black")
btn_frame.pack(pady=10)

BTN = dict(font=("times", 13, "bold"), width=22, height=2, bd=5, relief=RIDGE)

tk.Button(btn_frame, text="1. Capture Face Images",
          bg="green", fg="white", command=do_capture,
          **BTN).grid(row=0, column=0, padx=14, pady=8)

tk.Button(btn_frame, text="2. Train Model",
          bg="blue", fg="white", command=do_train,
          **BTN).grid(row=0, column=1, padx=14, pady=8)

tk.Button(btn_frame, text="3. Auto Attendance (Face)",
          bg="purple", fg="white", command=do_auto_attendance,
          **BTN).grid(row=1, column=0, padx=14, pady=8)

tk.Button(btn_frame, text="4. Manual Attendance",
          bg="orange", fg="black", command=do_manual_attendance,
          **BTN).grid(row=1, column=1, padx=14, pady=8)

tk.Button(btn_frame, text="5. View Attendance",
          bg="red", fg="white", command=do_view_attendance,
          **BTN).grid(row=2, column=0, padx=14, pady=8)

tk.Button(btn_frame, text="Exit",
          bg="gray", fg="white", command=window.destroy,
          **BTN).grid(row=2, column=1, padx=14, pady=8)

window.mainloop()
