import pandas as pd
from glob import glob
import os
import csv
import tkinter as tk
from tkinter import *
import sys
import subprocess
import tkinter.messagebox as mb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def subjectchoose(text_to_speech):

    def calculate_attendance():
        Subject = tx.get().strip()
        if Subject == "":
            text_to_speech("Please enter the subject name.")
            return

        pattern = os.path.join(BASE_DIR, "Attendance", Subject, f"{Subject}*.csv")
        filenames = [f for f in glob(pattern) if "summary" not in f]

        if not filenames:
            t = f"No attendance files found for: {Subject}"
            text_to_speech(t)
            mb.showinfo("No files", t)
            return

        df_list = [pd.read_csv(f) for f in filenames]
        newdf = df_list[0]
        for i in range(1, len(df_list)):
            newdf = newdf.merge(df_list[i], how="outer")
        newdf.fillna(0, inplace=True)

        date_cols = [c for c in newdf.columns if c not in ("Enrollment", "Name", "Attendance", "Date", "Time")]
        if date_cols:
            newdf["Attendance"] = newdf[date_cols].apply(
                lambda row: str(int(round(
                    pd.to_numeric(row, errors="coerce").fillna(0).mean() * 100
                ))) + "%",
                axis=1
            )
        else:
            newdf["Attendance"] = "0%"

        out_dir = os.path.join(BASE_DIR, "Attendance", Subject)
        os.makedirs(out_dir, exist_ok=True)
        out_csv = os.path.join(out_dir, "attendance_summary.csv")
        newdf.to_csv(out_csv, index=False)

        # use Toplevel so we don't create a second Tk root (causes freeze)
        top = tk.Toplevel(subject)
        top.title("Attendance of " + Subject)
        top.configure(background="black")

        with open(out_csv) as file:
            reader = csv.reader(file)
            for r, col in enumerate(reader):
                for c, val in enumerate(col):
                    tk.Label(
                        top,
                        width=14, height=1,
                        fg="yellow",
                        font=("times", 13, "bold"),
                        bg="black",
                        text=val,
                        relief=RIDGE,
                    ).grid(row=r, column=c, padx=1, pady=1)

    # ── subject window ────────────────────────────────────────────
    subject = tk.Tk()
    subject.title("View Attendance")
    subject.geometry("600x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    tk.Label(subject, bg="black", relief=RIDGE, bd=10,
             font=("arial", 30)).pack(fill=X)

    tk.Label(
        subject,
        text="Which Subject Attendance?",
        bg="black", fg="green",
        font=("arial", 22),
    ).place(x=90, y=12)

    tk.Label(
        subject, text="Enter Subject",
        width=10, height=2,
        bg="black", fg="yellow",
        bd=5, relief=RIDGE,
        font=("times new roman", 15),
    ).place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15, bd=5,
        bg="black", fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=200, y=100)

    def open_folder():
        sub = tx.get().strip()
        if sub == "":
            text_to_speech("Please enter the subject name.")
            return
        subj_path = os.path.join(BASE_DIR, "Attendance", sub)
        if not os.path.exists(subj_path):
            t = f"No attendance folder found for {sub}"
            text_to_speech(t)
            mb.showinfo("Not found", t)
            return
        try:
            if sys.platform.startswith("darwin"):
                subprocess.call(["open", subj_path])
            elif sys.platform.startswith("win"):
                os.startfile(subj_path)
            else:
                subprocess.call(["xdg-open", subj_path])
        except Exception as e:
            mb.showinfo("Error", f"Could not open folder: {e}")

    tk.Button(
        subject, text="View Attendance",
        command=calculate_attendance,
        bd=7, font=("times new roman", 15),
        bg="black", fg="yellow",
        height=2, width=13, relief=RIDGE,
    ).place(x=160, y=200)

    tk.Button(
        subject, text="Check Sheets",
        command=open_folder,
        bd=7, font=("times new roman", 15),
        bg="black", fg="yellow",
        height=2, width=10, relief=RIDGE,
    ).place(x=400, y=200)

    subject.mainloop()
