import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

import face_dataset
import trainer
import attendance_cam
import camera_test

attendance_file = "attendance.csv"

# ---------------- Functions ----------------
def register_student():
    # New window for student registration
    reg_win = tk.Toplevel(root)
    reg_win.title("Register Student")
    reg_win.geometry("400x200")

    tk.Label(reg_win, text="Student ID:", font=("Arial", 12)).pack(pady=5)
    entry_id = tk.Entry(reg_win, font=("Arial", 12))
    entry_id.pack(pady=5)

    tk.Label(reg_win, text="Student Name:", font=("Arial", 12)).pack(pady=5)
    entry_name = tk.Entry(reg_win, font=("Arial", 12))
    entry_name.pack(pady=5)

    def start_reg():
        student_id = entry_id.get()
        name = entry_name.get()

        if not student_id or not name:
            messagebox.showerror("Error", "Both ID and Name are required!", parent=reg_win)
            return

        reg_win.destroy()  # close the form window
        face_dataset.start_registration(student_id, name)
        messagebox.showinfo("Success", f"Student {name} registered successfully!")

    tk.Button(reg_win, text="Start Registration", font=("Arial", 12), bg="#4CAF50", fg="white",
              command=start_reg).pack(pady=10)


def train_model_gui():
    trainer.train_model()
    messagebox.showinfo("Training", "✅ Model training complete!")


def take_attendance_gui():
    attendance_cam.recognize()
    messagebox.showinfo("attendance","attendance marked successfully")


def camera_test_gui():
    camera_test.main()


def view_attendance():
    if not os.path.exists(attendance_file):
        messagebox.showinfo("Info", "Attendance file not found!")
        return

    win = tk.Toplevel(root)
    win.title("Attendance Records")
    win.geometry("600x400")

    tree = ttk.Treeview(win, columns=("ID", "Name", "Date", "Time"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.pack(fill=tk.BOTH, expand=True)

    with open(attendance_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            tree.insert("", tk.END, values=row)


# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

title = tk.Label(root, text="Attendance System", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="blue")
title.pack(pady=20)

btn1 = tk.Button(root, text="📸 Register Student", font=("Arial", 14), bg="#4CAF50", fg="white", width=25,
                 command=register_student)
btn1.pack(pady=10)

btn3 = tk.Button(root, text="✅ Take Attendance", font=("Arial", 14), bg="#FF9800", fg="white", width=25,
                 command=take_attendance_gui)
btn3.pack(pady=10)

btn4 = tk.Button(root, text="📊 View Attendance", font=("Arial", 14), bg="#9C27B0", fg="white", width=25,
                 command=view_attendance)
btn4.pack(pady=10)

btn5 = tk.Button(root, text="📷 Test Camera", font=("Arial", 14), bg="#795548", fg="white", width=25,
                 command=camera_test_gui)
btn5.pack(pady=10)

btn_exit = tk.Button(root, text="❌ Exit", font=("Arial", 14), bg="red", fg="white", width=25, command=root.quit)
btn_exit.pack(pady=20)

root.mainloop()
