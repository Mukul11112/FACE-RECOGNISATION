import tkinter as tk
from tkinter import *
import os
import csv
import pandas as pd
import datetime
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ts = time.time()
Date = datetime.datetime.fromtimestamp(ts).strftime("%Y_%m_%d")
timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
Hour, Minute, Second = timeStamp.split(":")


def manually_fill():
    d = {}
    index = [0]  # list so nested functions can mutate it

    sb = tk.Tk()
    # NOTE: removed iconbitmap("AMS.ico") — crashes if icon file is missing
    sb.title("Manual Attendance")
    sb.geometry("580x320")
    sb.configure(background="black")

    def err_screen_for_subject():
        # use Toplevel NOT a second Tk() — second Tk() causes crash/freeze
        ec = tk.Toplevel(sb)
        ec.geometry("340x110")
        ec.title("Warning!")
        ec.configure(background="black")
        tk.Label(ec, text="Please enter subject name!",
                 fg="red", bg="black", font=("times", 15, "bold")).pack(pady=15)
        tk.Button(ec, text="OK", command=ec.destroy,
                  fg="black", bg="lawn green", width=9,
                  font=("times", 13, "bold")).pack()

    def fill_attendance():
        subb = SUB_ENTRY.get().strip()
        if subb == "":
            err_screen_for_subject()
            return

        sb.destroy()

        MFW = tk.Tk()
        MFW.title("Manual Attendance — " + subb)
        MFW.geometry("880x500")
        MFW.configure(background="black")

        def err_screen1():
            # Toplevel instead of second Tk()
            errsc = tk.Toplevel(MFW)
            errsc.geometry("380x110")
            errsc.title("Warning!")
            errsc.configure(background="black")
            tk.Label(errsc, text="Please enter Enrollment & Student name!",
                     fg="red", bg="black", font=("times", 14, "bold")).pack(pady=15)
            tk.Button(errsc, text="OK", command=errsc.destroy,
                      fg="black", bg="lawn green", width=9,
                      font=("times", 13, "bold")).pack()

        def testVal(inStr, acttyp):
            if acttyp == "1":
                if not inStr.isdigit():
                    return False
            return True

        tk.Label(MFW, text="Enter Enrollment", width=15, height=2,
                 fg="white", bg="blue2", font=("times", 15, "bold")).place(x=30, y=100)

        tk.Label(MFW, text="Enter Student Name", width=15, height=2,
                 fg="white", bg="blue2", font=("times", 15, "bold")).place(x=30, y=200)

        ENR_ENTRY = tk.Entry(MFW, width=20, validate="key",
                             bg="yellow", fg="red", font=("times", 23, "bold"))
        ENR_ENTRY["validatecommand"] = (ENR_ENTRY.register(testVal), "%P", "%d")
        ENR_ENTRY.place(x=290, y=105)

        STUDENT_ENTRY = tk.Entry(MFW, width=20, bg="yellow", fg="red",
                                 font=("times", 23, "bold"))
        STUDENT_ENTRY.place(x=290, y=205)

        Notifi = tk.Label(MFW, text="", bg="black", fg="white",
                          width=45, height=2, font=("times", 14, "bold"))
        Notifi.place(x=80, y=390)

        def enter_data_DB():
            ENROLLMENT = ENR_ENTRY.get().strip()
            STUDENT = STUDENT_ENTRY.get().strip()
            if ENROLLMENT == "" or STUDENT == "":
                err_screen1()
                return
            d[index[0]] = {"Enrollment": ENROLLMENT, "Name": STUDENT, Date: 1}
            index[0] += 1
            ENR_ENTRY.delete(0, "end")
            STUDENT_ENTRY.delete(0, "end")
            Notifi.configure(
                text=f"Added: {STUDENT} ({ENROLLMENT}) — Total: {index[0]}",
                bg="blue2")

        def create_csv():
            if not d:
                Notifi.configure(text="No data entered yet!", bg="red")
                return

            # .T fixes orientation — original pd.DataFrame(d) produced wrong table
            df = pd.DataFrame(d).T.reset_index(drop=True)

            # save to project-local folder (original had hardcoded Windows path)
            out_dir = os.path.join(BASE_DIR, "Attendance", subb)
            os.makedirs(out_dir, exist_ok=True)
            csv_name = os.path.join(
                out_dir, f"{subb}_{Date}_{Hour}-{Minute}-{Second}.csv")
            df.to_csv(csv_name, index=False)
            Notifi.configure(text=f"Saved: {csv_name}", bg="green")

        def open_folder():
            import subprocess, sys
            folder = os.path.join(BASE_DIR, "Attendance", subb)
            os.makedirs(folder, exist_ok=True)
            # cross-platform — removed hardcoded C:/Users/patel/... path
            if sys.platform.startswith("darwin"):
                subprocess.call(["open", folder])
            elif sys.platform.startswith("win"):
                os.startfile(folder)
            else:
                subprocess.call(["xdg-open", folder])

        tk.Button(MFW, text="Clear",
                  command=lambda: ENR_ENTRY.delete(0, "end"),
                  fg="black", bg="deep pink", width=10,
                  font=("times", 13, "bold")).place(x=695, y=108)

        tk.Button(MFW, text="Clear",
                  command=lambda: STUDENT_ENTRY.delete(0, "end"),
                  fg="black", bg="deep pink", width=10,
                  font=("times", 13, "bold")).place(x=695, y=208)

        tk.Button(MFW, text="Enter Data", command=enter_data_DB,
                  fg="black", bg="lime green", width=20, height=2,
                  font=("times", 15, "bold")).place(x=80, y=300)

        tk.Button(MFW, text="Save to CSV", command=create_csv,
                  fg="white", bg="red", width=20, height=2,
                  font=("times", 15, "bold")).place(x=430, y=300)

        tk.Button(MFW, text="Check Sheets", command=open_folder,
                  fg="black", bg="lawn green", width=12,
                  font=("times", 13, "bold")).place(x=730, y=440)

        MFW.mainloop()

    # ── subject entry window ──────────────────────────────────────
    tk.Label(sb, text="Manual Attendance Entry",
             bg="black", fg="green",
             font=("arial", 20, "bold")).pack(pady=20)

    tk.Label(sb, text="Enter Subject", width=15, height=2,
             fg="white", bg="blue2",
             font=("times", 15, "bold")).place(x=30, y=100)

    SUB_ENTRY = tk.Entry(sb, width=20, bg="yellow", fg="red",
                         font=("times", 23, "bold"))
    SUB_ENTRY.place(x=250, y=105)

    tk.Button(sb, text="Fill Attendance", command=fill_attendance,
              fg="white", bg="deep pink", width=20, height=2,
              font=("times", 15, "bold")).place(x=250, y=180)

    sb.mainloop()
