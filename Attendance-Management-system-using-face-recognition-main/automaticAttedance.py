import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import os, cv2
import csv
import pandas as pd
import datetime
import time

def subjectChoose(text_to_speech):
    subject_win = ctk.CTkToplevel()
    subject_win.title("Take Attendance Scanner")
    subject_win.geometry("600x400")
    subject_win.grab_set()
    subject_win.configure(fg_color=("#f8fafc", "#161616"))
    
    title_lbl = ctk.CTkLabel(subject_win, text="Take Live Attendance", font=ctk.CTkFont(size=30, weight="bold"), text_color=("#1e293b", "white"))
    title_lbl.pack(pady=(30, 10))
    
    sub_lbl = ctk.CTkLabel(subject_win, text="Enter the subject name to start the facial recognition scanner.", font=ctk.CTkFont(size=14), text_color=("#64748b", "gray"))
    sub_lbl.pack(pady=(0, 20))
    
    form = ctk.CTkFrame(subject_win, corner_radius=15, fg_color=("#ffffff", "#1e1e1e"), border_color=("#e2e8f0", "#333"), border_width=1)
    form.pack(pady=10, padx=50, fill="both", expand=True)
    
    tx = ctk.CTkEntry(form, width=300, height=45, placeholder_text="Subject Name (e.g., Math)", font=ctk.CTkFont(size=16), fg_color=("#f1f5f9", "#333333"), border_color=("#cbd5e1", "#444"))
    tx.pack(pady=(40, 20))
    tx.bind("<FocusIn>", lambda e: tx.configure(border_color="#3b82f6"))
    tx.bind("<FocusOut>", lambda e: tx.configure(border_color=("#cbd5e1", "#444")))
    
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            text_to_speech("Please enter the subject name")
            messagebox.showwarning("Warning", "Subject Name is required!")
            return
            
        haarcasecade_path = "haarcascade_frontalface_default.xml"
        trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
        studentdetail_path = "StudentDetails/studentdetails.csv"
        attendance_path = "Attendance"
        
        if not os.path.exists(trainimagelabel_path):
            text_to_speech("Model not found")
            messagebox.showerror("Error", "Model not found, please train model first.")
            return
            
        try:
            df = pd.read_csv(studentdetail_path)
            df['Enrollment'] = pd.to_numeric(df['Enrollment'], errors='coerce')
        except Exception as e:
            messagebox.showerror("Error", "Could not read student details database.")
            return
            
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainimagelabel_path)
        facecasCade = cv2.CascadeClassifier(haarcasecade_path)
        
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            messagebox.showerror("Error", "Webcam not detected. Please connect a webcam.")
            return
            
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ["Id", "Name", "Date", "Time"]
        attendance = pd.DataFrame(columns=col_names)
        
        now = time.time()
        future = now + 15 # Run scanner for 15 seconds
        
        text_to_speech("Scanning started")
        
        while True:
            ret, im = cam.read()
            if not ret:
                break
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = facecasCade.detectMultiScale(gray, 1.2, 5)
            
            for (x, y, w, h) in faces:
                Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                if conf < 70:
                    ts = time.time()
                    date_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                    time_str = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
                    
                    try:
                        matches = df.loc[df["Enrollment"] == Id]
                        if not matches.empty:
                            aa = matches["Name"].values[0]
                        else:
                            aa = "Unknown"
                    except:
                        aa = "Unknown"
                        
                    tt = str(Id) + "-" + str(aa)
                    
                    attendance.loc[len(attendance)] = [Id, aa, date_str, time_str]
                    
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 4)
                    cv2.putText(im, str(tt), (x, y - 10), font, 0.8, (255, 255, 0), 2)
                else:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 4)
                    cv2.putText(im, "Unknown", (x, y - 10), font, 0.8, (0, 25, 255), 2)
                    
            cv2.imshow("Live Attendance Scanner", im)
            
            if time.time() > future:
                break
            if cv2.waitKey(30) & 0xFF == 27: # ESC
                break
                
        cam.release()
        cv2.destroyAllWindows()
        
        attendance = attendance.drop_duplicates(["Id"], keep="first")
        if len(attendance) > 0:
            ts = time.time()
            date_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            
            os.makedirs(attendance_path, exist_ok=True)
            fileName = os.path.join(attendance_path, f"Attendance_{date_str}.csv")
            
            # Format output correctly for our dashboard table
            if os.path.exists(fileName):
                attendance.to_csv(fileName, mode='a', header=False, index=False)
            else:
                attendance.to_csv(fileName, index=False)
                
            # De-duplicate the entire file after appending
            try:
                full_df = pd.read_csv(fileName)
                full_df = full_df.drop_duplicates(subset=["Id"], keep="first")
                full_df.to_csv(fileName, index=False)
            except:
                pass
                
            text_to_speech("Attendance Filled Successfully")
            messagebox.showinfo("Success", f"Attendance for {len(attendance)} students recorded!")
            subject_win.destroy()
        else:
            text_to_speech("No faces detected")
            messagebox.showwarning("Warning", "No registered faces were detected during the scan.")

    btn = ctk.CTkButton(form, text="Start Scanner", width=300, height=45, font=ctk.CTkFont(weight="bold", size=15), cursor="hand2", command=FillAttendance)
    btn.pack(pady=(0, 20))
    btn.bind("<Enter>", lambda e: btn.configure(fg_color="#2563eb"))
    btn.bind("<Leave>", lambda e: btn.configure(fg_color="#1f6aa5"))
    
    subject_win.wait_window()
