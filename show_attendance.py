import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *
import sys
import subprocess
import tkinter.messagebox as mb

# base dir
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if Subject=="":
            t='Please enter the subject name.'
            text_to_speech(t)
        # find attendance CSV files for the subject
        pattern = os.path.join(BASE_DIR, "Attendance", Subject, f"{Subject}*.csv")
        filenames = glob(pattern)
        if not filenames:
            t = f"No attendance files found for subject {Subject}."
            text_to_speech(t)
            try:
                mb.showinfo("No files", t)
            except Exception:
                pass
            return

        df_list = [pd.read_csv(f) for f in filenames]
        newdf = df_list[0]
        for i in range(1, len(df_list)):
            # merge on common columns (outer to preserve all enrollments)
            newdf = newdf.merge(df_list[i], how="outer")
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = 0
        # compute attendance percentage across date columns (assume first two cols are Enrollment, Name)
        if newdf.shape[1] <= 2:
            # no date columns
            for i in range(len(newdf)):
                newdf.at[i, "Attendance"] = "0%"
        else:
            date_cols = newdf.columns[2:]
            for i in range(len(newdf)):
                try:
                    vals = newdf.iloc[i, 2:-1].astype(float)
                    pct = int(round(vals.mean() * 100))
                except Exception:
                    # fallback if casting fails
                    vals = newdf.iloc[i, 2:-1].fillna(0)
                    try:
                        pct = int(round(vals.mean() * 100))
                    except Exception:
                        pct = 0
                newdf.at[i, "Attendance"] = str(pct) + '%'
            #newdf.sort_values(by=['Enrollment'],inplace=True)
        out_dir = os.path.join(BASE_DIR, "Attendance", Subject)
        os.makedirs(out_dir, exist_ok=True)
        out_csv = os.path.join(out_dir, "attendance.csv")
        newdf.to_csv(out_csv, index=False)

        root = tkinter.Tk()
        root.title("Attendance of "+Subject)
        root.configure(background="black")
        cs = out_csv
        with open(cs) as file:
            reader = csv.reader(file)
            r = 0

            for col in reader:
                c = 0
                for row in col:

                    label = tkinter.Label(
                        root,
                        width=10,
                        height=1,
                        fg="yellow",
                        font=("times", 15, " bold "),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                    )
                    label.grid(row=r, column=c)
                    c += 1
                r += 1
        root.mainloop()
        print(newdf)

    subject = Tk()
    # windo.iconbitmap("AMS.ico")
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")
    # subject_logo = Image.open("UI_Image/0004.png")
    # subject_logo = subject_logo.resize((50, 47), Image.ANTIALIAS)
    # subject_logo1 = ImageTk.PhotoImage(subject_logo)
    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)
    # l1 = tk.Label(subject, image=subject_logo1, bg="black",)
    # l1.place(x=100, y=10)
    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get()
        if sub == "":
            t="Please enter the subject name!!!"
            text_to_speech(t)
        else:
            subj_path = os.path.join(BASE_DIR, "Attendance", sub)
            if not os.path.exists(subj_path):
                t = f"No attendance found for subject {sub}"
                text_to_speech(t)
                try:
                    mb.showinfo("Not found", t)
                except Exception:
                    pass
                return
            try:
                if sys.platform.startswith("darwin"):
                    subprocess.call(["open", subj_path])
                elif sys.platform.startswith("win"):
                    os.startfile(subj_path)
                else:
                    subprocess.call(["xdg-open", subj_path])
            except Exception as e:
                text_to_speech("Unable to open folder")
                try:
                    mb.showinfo("Error", f"Could not open folder: {e}")
                except Exception:
                    pass


    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=10,
        relief=RIDGE,
    )
    attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)
    subject.mainloop()
