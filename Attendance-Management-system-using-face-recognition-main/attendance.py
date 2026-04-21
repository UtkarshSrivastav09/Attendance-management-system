import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
import os, cv2
import shutil
import csv
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time
import pyttsx3
import json
import subprocess

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

def get_student_count():
    try:
        if os.path.exists(studentdetail_path):
            df = pd.read_csv(studentdetail_path)
            return len(df)
    except:
        pass
    return 0

def get_attendance_count_today():
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(attendance_path, f"Attendance_{today}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return len(df)
    except:
        pass
    return 0
    
def get_last_7_days_attendance():
    counts = []
    dates = []
    for i in range(6, -1, -1):
        target_date = datetime.datetime.now() - datetime.timedelta(days=i)
        date_str = target_date.strftime("%Y-%m-%d")
        dates.append(target_date.strftime("%m-%d"))
        
        file_path = os.path.join(attendance_path, f"Attendance_{date_str}.csv")
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                counts.append(len(df))
            except:
                counts.append(0)
        else:
            counts.append(0)
    return dates, counts

def get_today_logs():
    try:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        file_path = os.path.join(attendance_path, f"Attendance_{today}.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            return df.values.tolist()
    except:
        pass
    return []

def err_screen():
    messagebox.showwarning("Warning", "Enrollment & Name required!!!")

class StatCard(ctk.CTkFrame):
    def __init__(self, master, title, value, **kwargs):
        super().__init__(master, corner_radius=10, fg_color=("#ffffff", "#1e1e1e"), border_color=("#e2e8f0", "#333333"), border_width=1, **kwargs)
        
        self.title_lbl = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=14), text_color=("#64748b", "gray"))
        self.title_lbl.pack(anchor="w", padx=20, pady=(15, 0))
        
        self.value_lbl = ctk.CTkLabel(self, text=str(value), font=ctk.CTkFont(size=36, weight="bold"), text_color="#1f6aa5")
        self.value_lbl.pack(anchor="w", padx=20, pady=(0, 15))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Face Recognition Attendance System - Dashboard")
        self.geometry("1400x850")
        self.minsize(1200, 750)
        self.after(0, lambda: self.state('zoomed'))
        self.configure(fg_color=("#f1f5f9", "#101010"))
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.main_frame = MainFrame(self, self.logout)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.refresh_stats()
        
    def logout(self):
        self.destroy()
        subprocess.Popen(["python", "auth.py"])

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, logout_callback):
        super().__init__(master, fg_color="transparent")
        self.master = master
        self.logout_callback = logout_callback
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- Sidebar ---
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0, fg_color=("#ffffff", "#161616"), border_color=("#e2e8f0", "#222"), border_width=1)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        
        try:
            logo = ctk.CTkImage(Image.open("UI_Image/0001.png"), size=(40, 40))
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text=" SmartCampus\n Attendance System", image=logo, compound="left", font=ctk.CTkFont(size=18, weight="bold"), text_color=("#1e293b", "white"), justify="left")
        except:
            self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="SmartCampus\nAttendance System", font=ctk.CTkFont(size=18, weight="bold"), text_color=("#1e293b", "white"), justify="left")
        
        self.logo_label.grid(row=0, column=0, padx=20, pady=(40, 40))
        
        # Sidebar Menu
        self.menu_lbl = ctk.CTkLabel(self.sidebar_frame, text="MAIN MENU", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#64748b", "gray"))
        self.menu_lbl.grid(row=1, column=0, padx=30, pady=(0, 10), sticky="w")
        
        self.btn_dash = ctk.CTkButton(self.sidebar_frame, text="Dashboard Analytics", fg_color="#1f6aa5", anchor="w", font=ctk.CTkFont(size=14, weight="bold"), height=45, cursor="hand2")
        self.btn_dash.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        # Action Buttons moved to Sidebar for PowerBI layout
        self.actions_lbl = ctk.CTkLabel(self.sidebar_frame, text="SYSTEM ACTIONS", font=ctk.CTkFont(size=12, weight="bold"), text_color=("#64748b", "gray"))
        self.actions_lbl.grid(row=4, column=0, padx=30, pady=(20, 10), sticky="w")
        
        self.btn_register = ctk.CTkButton(self.sidebar_frame, text="Register Student", fg_color="transparent", text_color=("#1e293b", "white"), hover_color=("#e2e8f0", "#2b2b2b"), anchor="w", font=ctk.CTkFont(size=14), height=45, cursor="hand2", command=self.open_register_window)
        self.btn_register.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_take_att = ctk.CTkButton(self.sidebar_frame, text="Take Attendance", fg_color="transparent", text_color=("#1e293b", "white"), hover_color=("#e2e8f0", "#2b2b2b"), anchor="w", font=ctk.CTkFont(size=14), height=45, cursor="hand2", command=self.take_attendance)
        self.btn_take_att.grid(row=6, column=0, padx=20, pady=5, sticky="ew")
        
        self.btn_view_rep = ctk.CTkButton(self.sidebar_frame, text="View Reports", fg_color="transparent", text_color=("#1e293b", "white"), hover_color=("#e2e8f0", "#2b2b2b"), anchor="w", font=ctk.CTkFont(size=14), height=45, cursor="hand2", command=self.view_attendance)
        self.btn_view_rep.grid(row=7, column=0, padx=20, pady=5, sticky="ew")

        # Theme Button
        self.theme_btn = ctk.CTkButton(self.sidebar_frame, text="Theme: ☀️" if ctk.get_appearance_mode()=="Light" else "Theme: 🌙", command=self.toggle_theme, font=ctk.CTkFont(size=14, weight="bold"), cursor="hand2", fg_color=("#e2e8f0", "#2b2b2b"), text_color=("#0f172a", "white"), hover_color=("#cbd5e1", "#3d3d3d"), height=45)
        self.theme_btn.grid(row=9, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_logout = ctk.CTkButton(self.sidebar_frame, text="Sign Out", fg_color="transparent", hover_color=("#fee2e2", "#3d1c1c"), text_color="#ff4d4d", anchor="w", font=ctk.CTkFont(size=14, weight="bold"), height=45, command=self.logout_callback, cursor="hand2")
        self.btn_logout.grid(row=10, column=0, padx=20, pady=30, sticky="ew")
        
        # --- Main Content (Power BI Layout) ---
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(2, weight=1) # Charts
        self.content_frame.grid_rowconfigure(3, weight=1) # Table
        
        # Header
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.welcome_lbl = ctk.CTkLabel(self.header_frame, text="Dashboard", font=ctk.CTkFont(size=32, weight="bold"), text_color=("#1e293b", "white"))
        self.welcome_lbl.pack(side="left")
        
        self.refresh_btn = ctk.CTkButton(self.header_frame, text="↻ Refresh Analytics", font=ctk.CTkFont(weight="bold", size=14), fg_color="#2da84a", hover_color="#207a35", cursor="hand2", command=self.force_refresh)
        self.refresh_btn.pack(side="right", pady=10, padx=(20, 0))
        
        self.date_lbl = ctk.CTkLabel(self.header_frame, text="", font=ctk.CTkFont(size=14), text_color=("#64748b", "gray"))
        self.date_lbl.pack(side="right", pady=10)
        self.update_clock()
        
        # Stats Row
        self.stats_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        self.stat1 = StatCard(self.stats_frame, "Total Registered Students", "0")
        self.stat1.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.stat2 = StatCard(self.stats_frame, "Classes Attended Today", "0")
        self.stat2.grid(row=0, column=1, sticky="ew", padx=10)
        
        self.stat3 = StatCard(self.stats_frame, "System Status", "Online")
        self.stat3.value_lbl.configure(text_color="#2da84a")
        self.stat3.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        
        # Charts Row
        self.charts_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.charts_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        self.charts_frame.grid_columnconfigure(0, weight=2) # Bar chart takes more space
        self.charts_frame.grid_columnconfigure(1, weight=1) # Pie chart
        
        self.fig_bg_color = "#1e1e1e" if ctk.get_appearance_mode() == "Dark" else "#ffffff"
        self.fig_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "#1e293b"
        
        # Table Row
        self.table_frame = ctk.CTkFrame(self.content_frame, fg_color=("#ffffff", "#1e1e1e"), corner_radius=10, border_width=1, border_color=("#e2e8f0", "#333333"))
        self.table_frame.grid(row=3, column=0, sticky="nsew")
        self.table_frame.grid_rowconfigure(1, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)
        
        tbl_lbl = ctk.CTkLabel(self.table_frame, text="Live Attendance Feed", font=ctk.CTkFont(size=18, weight="bold"), text_color=("#1e293b", "white"))
        tbl_lbl.grid(row=0, column=0, sticky="w", padx=20, pady=15)
        
        # ttk styling for Treeview
        style = ttk.Style()
        style.theme_use("default")
        
        # Medium font size for table data
        style.configure("Treeview", font=('Helvetica', 12), background="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f8fafc", foreground="white" if ctk.get_appearance_mode() == "Dark" else "black", rowheight=35, fieldbackground="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f8fafc", borderwidth=0)
        style.map('Treeview', background=[('selected', '#1f6aa5')])
        
        # Medium font size for table headings
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white", relief="flat", font=('Helvetica', 13, 'bold'))
        style.map("Treeview.Heading", background=[('active', '#144870')])
        
        self.tree = ttk.Treeview(self.table_frame, columns=("ID", "Name", "Date", "Time"), show="headings")
        self.tree.heading("ID", text="Student ID")
        self.tree.heading("Name", text="Full Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Time", text="Check-In Time")
        
        self.tree.column("ID", anchor="center", width=100)
        self.tree.column("Name", anchor="center", width=300)
        self.tree.column("Date", anchor="center", width=150)
        self.tree.column("Time", anchor="center", width=150)
        
        self.tree.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        self.draw_charts()

    def draw_charts(self):
        # Prevent focus errors by taking focus to the main window and closing pyplot event loops
        self.focus_set()
        plt.close('all')
        
        # Clear previous charts
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
            
        self.fig_bg_color = "#1e1e1e" if ctk.get_appearance_mode() == "Dark" else "#ffffff"
        self.fig_text_color = "white" if ctk.get_appearance_mode() == "Dark" else "#1e293b"
        
        # 1. Bar Chart (7 Days)
        dates, counts = get_last_7_days_attendance()
        
        fig1, ax1 = plt.subplots(figsize=(6, 3.5), facecolor=self.fig_bg_color)
        bars = ax1.bar(dates, counts, color="#1f6aa5", edgecolor=self.fig_bg_color, linewidth=2)
        ax1.set_facecolor(self.fig_bg_color)
        ax1.set_title("Attendance Trends (Last 7 Days)", color=self.fig_text_color, fontsize=14, pad=15)
        ax1.tick_params(colors=self.fig_text_color)
        for spine in ax1.spines.values():
            spine.set_visible(False)
        ax1.grid(axis='y', linestyle='--', alpha=0.3, color="gray")
        
        # Add values on top of bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{int(height)}', ha='center', va='bottom', color=self.fig_text_color)

        plt.tight_layout()
        
        chart_frame1 = ctk.CTkFrame(self.charts_frame, corner_radius=10, fg_color=self.fig_bg_color, border_width=1, border_color=("#e2e8f0", "#333333"))
        chart_frame1.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        canvas1 = FigureCanvasTkAgg(fig1, master=chart_frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        # 2. Doughnut Chart (Present vs Absent)
        total_students = get_student_count()
        today_att = get_attendance_count_today()
        absent = max(0, total_students - today_att)
        
        fig2, ax2 = plt.subplots(figsize=(4, 3.5), facecolor=self.fig_bg_color)
        
        if total_students == 0:
            labels = ["No Data"]
            sizes = [1]
            colors = ["gray"]
        else:
            labels = ['Present', 'Absent']
            sizes = [today_att, absent]
            colors = ['#2da84a', '#ff4d4d']
            
        wedges, texts, autotexts = ax2.pie(
            sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
            textprops=dict(color=self.fig_text_color, fontsize=12, fontweight='bold'),
            wedgeprops=dict(width=0.4, edgecolor=self.fig_bg_color, linewidth=2),
            radius=0.72, center=(0, 0.28)
        )
        
        # Increase the size of the percentage labels so they look better
        for autotext in autotexts:
            autotext.set_fontsize(14)
            
        # Guarantee a perfect, centered circle without stretching
        ax2.axis('equal')
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-0.45, 0.5)
        
        # Move the title text further up
        ax2.set_title("Today's Attendance Rate", color=self.fig_text_color, fontsize=16, fontweight='bold', y=1.08)
        
        # Add Interactive Hover Annotation
        annot = ax2.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points",
                             bbox=dict(boxstyle="round,pad=0.5", fc=self.fig_bg_color, ec="gray", alpha=0.9),
                             color=self.fig_text_color, fontsize=12, fontweight='bold')
        annot.set_visible(False)

        def hover(event):
            if event.inaxes == ax2:
                for i, wedge in enumerate(wedges):
                    cont, _ = wedge.contains(event)
                    if cont:
                        annot.xy = (event.xdata, event.ydata)
                        text = f"{labels[i]}: {sizes[i]} Students"
                        annot.set_text(text)
                        annot.set_visible(True)
                        fig2.canvas.draw_idle()
                        return
                if annot.get_visible():
                    annot.set_visible(False)
                    fig2.canvas.draw_idle()

        fig2.canvas.mpl_connect("motion_notify_event", hover)
        
        # Use tight_layout to mathematically guarantee nothing gets cut off on any screen size
        fig2.tight_layout()
        
        chart_frame2 = ctk.CTkFrame(self.charts_frame, corner_radius=10, fg_color=self.fig_bg_color, border_width=1, border_color=("#e2e8f0", "#333333"))
        chart_frame2.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
        canvas2 = FigureCanvasTkAgg(fig2, master=chart_frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="Theme: ☀️")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="Theme: 🌙")
            
        # Re-draw charts with new theme colors
        self.draw_charts()
        
        # Update Treeview style
        style = ttk.Style()
        style.configure("Treeview", background="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f8fafc", foreground="white" if ctk.get_appearance_mode() == "Dark" else "black", fieldbackground="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f8fafc")

    def update_clock(self):
        if not self.winfo_exists():
            return
        now = datetime.datetime.now()
        self.date_lbl.configure(text=now.strftime("%A, %B %d, %Y | %I:%M %p"))
        self.after(60000, self.update_clock)
        
    def force_refresh(self):
        self.refresh_stats()
        self.draw_charts()
        
    def refresh_stats(self):
        students = get_student_count()
        today_att = get_attendance_count_today()
        self.stat1.value_lbl.configure(text=str(students))
        self.stat2.value_lbl.configure(text=str(today_att))
        
        # Update Table
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        logs = get_today_logs()
        for log in logs:
            self.tree.insert("", "end", values=log)

    def take_attendance(self):
        automaticAttedance.subjectChoose(text_to_speech)
        self.refresh_stats()
        self.draw_charts()

    def view_attendance(self):
        show_attendance.subjectchoose(text_to_speech)
        
    def open_register_window(self):
        reg_window = ctk.CTkToplevel(self.master)
        reg_window.title("Register Student")
        reg_window.geometry("800x600")
        reg_window.transient(self.master)
        reg_window.grab_set()
        reg_window.configure(fg_color=("#f8fafc", "#161616"))
        
        title = ctk.CTkLabel(reg_window, text="Register New Face", font=ctk.CTkFont(size=34, weight="bold"), text_color="#1f6aa5")
        title.pack(pady=(40, 10))
        
        sub = ctk.CTkLabel(reg_window, text="Enter student details below to start the training process.", font=ctk.CTkFont(size=14), text_color=("#64748b", "gray"))
        sub.pack(pady=(0, 30))
        
        form = ctk.CTkFrame(reg_window, corner_radius=20, fg_color=("#ffffff", "#1e1e1e"), border_color=("#e2e8f0", "#333"), border_width=1)
        form.pack(pady=10, padx=60, fill="both", expand=True)
        
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=2)
        
        # Enrollment
        ctk.CTkLabel(form, text="Enrollment No:", font=ctk.CTkFont(size=16, weight="bold"), text_color=("#1e293b", "white")).grid(row=0, column=0, pady=(50, 20), padx=30, sticky="e")
        enroll_entry = ctk.CTkEntry(form, height=45, font=ctk.CTkFont(size=16), fg_color=("#f8fafc", "#333333"), border_color=("#cbd5e1", "#444"))
        enroll_entry.grid(row=0, column=1, pady=(50, 20), padx=30, sticky="we")
        
        # Name
        ctk.CTkLabel(form, text="Full Name:", font=ctk.CTkFont(size=16, weight="bold"), text_color=("#1e293b", "white")).grid(row=1, column=0, pady=20, padx=30, sticky="e")
        name_entry = ctk.CTkEntry(form, height=45, font=ctk.CTkFont(size=16), fg_color=("#f8fafc", "#333333"), border_color=("#cbd5e1", "#444"))
        name_entry.grid(row=1, column=1, pady=20, padx=30, sticky="we")
        
        # Status
        ctk.CTkLabel(form, text="System Status:", font=ctk.CTkFont(size=16, weight="bold"), text_color=("#1e293b", "white")).grid(row=2, column=0, pady=20, padx=30, sticky="e")
        msg_label = ctk.CTkLabel(form, text="Ready", font=ctk.CTkFont(size=16), text_color="#2da84a")
        msg_label.grid(row=2, column=1, pady=20, padx=30, sticky="w")
        
        def do_take_image():
            e_no = enroll_entry.get()
            e_name = name_entry.get()
            if not e_no.isdigit():
                messagebox.showerror("Error", "Enrollment No must be a number!")
                return
            takeImage.TakeImage(e_no, e_name, haarcasecade_path, trainimage_path, msg_label, err_screen, text_to_speech)
            enroll_entry.delete(0, 'end')
            name_entry.delete(0, 'end')
            self.refresh_stats()
            self.draw_charts()
            
        def do_train_image():
            trainImage.TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, msg_label, text_to_speech)
            
        btn_frame = ctk.CTkFrame(reg_window, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        take_btn = ctk.CTkButton(btn_frame, text="1. Take Image", height=50, width=180, font=ctk.CTkFont(weight="bold", size=15), command=do_take_image, cursor="hand2")
        take_btn.grid(row=0, column=0, padx=20)
        
        train_btn = ctk.CTkButton(btn_frame, text="2. Train Model", height=50, width=180, font=ctk.CTkFont(weight="bold", size=15), fg_color="#2da84a", hover_color="#207a35", command=do_train_image, cursor="hand2")
        train_btn.grid(row=0, column=1, padx=20)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--dashboard":
        app = App()
        app.mainloop()
    else:
        import subprocess
        subprocess.Popen(["python", "auth.py"])
