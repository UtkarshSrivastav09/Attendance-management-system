import os
import pandas as pd
from glob import glob
import customtkinter as ctk
from tkinter import ttk, messagebox
import datetime

def subjectchoose(text_to_speech):
    rep_win = ctk.CTkToplevel()
    rep_win.title("Master Attendance Report")
    rep_win.geometry("900x600")
    rep_win.grab_set()
    rep_win.configure(fg_color=("#f8fafc", "#161616"))
    
    title_lbl = ctk.CTkLabel(rep_win, text="Master Attendance Report", font=ctk.CTkFont(size=30, weight="bold"), text_color=("#1e293b", "white"))
    title_lbl.pack(pady=(30, 10))
    
    sub_lbl = ctk.CTkLabel(rep_win, text="Aggregated attendance statistics across all tracked days.", font=ctk.CTkFont(size=14), text_color=("#64748b", "gray"))
    sub_lbl.pack(pady=(0, 20))
    
    table_frame = ctk.CTkFrame(rep_win, corner_radius=10, fg_color=("#ffffff", "#1e1e1e"), border_color=("#e2e8f0", "#333"), border_width=1)
    table_frame.pack(padx=30, pady=10, fill="both", expand=True)
    
    # Setup Treeview
    style = ttk.Style()
    style.configure("Report.Treeview", background="#2b2b2b" if ctk.get_appearance_mode() == "Dark" else "#f8fafc", foreground="white" if ctk.get_appearance_mode() == "Dark" else "black", rowheight=30, borderwidth=0)
    style.configure("Report.Treeview.Heading", background="#1f6aa5", foreground="white", relief="flat", font=('Helvetica', 11, 'bold'))
    style.map('Report.Treeview', background=[('selected', '#1f6aa5')])
    
    tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Total Days", "Present", "Percentage"), show="headings", style="Report.Treeview")
    tree.heading("ID", text="Student ID")
    tree.heading("Name", text="Full Name")
    tree.heading("Total Days", text="Total Tracked Days")
    tree.heading("Present", text="Days Present")
    tree.heading("Percentage", text="Attendance %")
    
    tree.column("ID", anchor="center", width=100)
    tree.column("Name", anchor="center", width=250)
    tree.column("Total Days", anchor="center", width=120)
    tree.column("Present", anchor="center", width=120)
    tree.column("Percentage", anchor="center", width=120)
    
    tree.pack(fill="both", expand=True, padx=20, pady=20)
    
    def calculate_master_report():
        # Get all attendance files
        attendance_dir = "Attendance"
        if not os.path.exists(attendance_dir):
            text_to_speech("No attendance data found.")
            messagebox.showinfo("Info", "No attendance records exist yet.")
            return
            
        files = glob(os.path.join(attendance_dir, "*.csv"))
        if len(files) == 0:
            text_to_speech("No attendance data found.")
            messagebox.showinfo("Info", "No attendance records exist yet.")
            return
            
        student_records = {} # {Id: {'Name': name, 'Present': count}}
        total_days = len(files)
        
        for file in files:
            try:
                df = pd.read_csv(file)
                # Deduplicate by ID just in case there are multiple entries for the same student on the same day
                df = df.drop_duplicates(subset=["Id"], keep="first")
                
                for _, row in df.iterrows():
                    sid = str(row["Id"])
                    name = row["Name"]
                    
                    if sid not in student_records:
                        student_records[sid] = {"Name": name, "Present": 0}
                    
                    student_records[sid]["Present"] += 1
            except:
                continue
                
        # Clear tree
        for item in tree.get_children():
            tree.delete(item)
            
        # Insert into tree and prepare master df
        report_data = []
        for sid, data in student_records.items():
            name = data["Name"]
            present = data["Present"]
            percentage = round((present / total_days) * 100)
            
            tree.insert("", "end", values=(sid, name, total_days, present, f"{percentage}%"))
            report_data.append([sid, name, total_days, present, f"{percentage}%"])
            
        # Save to master CSV
        if report_data:
            master_df = pd.DataFrame(report_data, columns=["Student ID", "Name", "Total Tracked Days", "Days Present", "Attendance %"])
            os.makedirs("Reports", exist_ok=True)
            report_path = os.path.join("Reports", "Master_Attendance_Report.csv")
            master_df.to_csv(report_path, index=False)
            
            text_to_speech("Master report generated successfully.")
            btn_open.configure(state="normal")
            
    def open_reports_folder():
        try:
            os.startfile(os.path.abspath("Reports"))
        except:
            pass
        
    btn_frame = ctk.CTkFrame(rep_win, fg_color="transparent")
    btn_frame.pack(pady=(10, 30))
    
    btn_generate = ctk.CTkButton(btn_frame, text="↻ Refresh Report", width=200, height=45, font=ctk.CTkFont(weight="bold", size=15), cursor="hand2", command=calculate_master_report)
    btn_generate.grid(row=0, column=0, padx=10)
    
    btn_open = ctk.CTkButton(btn_frame, text="Open Reports Folder", width=200, height=45, font=ctk.CTkFont(weight="bold", size=15), fg_color="#2da84a", hover_color="#207a35", cursor="hand2", state="disabled", command=open_reports_folder)
    btn_open.grid(row=0, column=1, padx=10)
    
    # Automatically generate when opened
    rep_win.after(500, calculate_master_report)
    
    # Wait for the window to close before returning
    rep_win.wait_window()
