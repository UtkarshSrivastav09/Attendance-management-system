import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import json
import os
import subprocess
from PIL import Image

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Smart College - Authentication")
        self.geometry("1100x650")
        self.minsize(900, 550)
        
        # Make the window run full screen directly
        self.after(0, lambda: self.state('zoomed'))
        
        self.users_file = "users.json"
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({"admin": "admin123"}, f)
                
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Left Panel with generated Background Image
        self.left_panel = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.left_panel.grid(row=0, column=0, sticky="nsew")
        
        try:
            bg_image = ctk.CTkImage(light_image=Image.open("UI_Image/login_bg_light.png"), dark_image=Image.open("UI_Image/login_bg.png"), size=(1000, 1000))
            self.bg_label = ctk.CTkLabel(self.left_panel, text="", image=bg_image)
            self.bg_label.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            self.left_panel.configure(fg_color=("#e0f2fe", "#0f172a")) # Fallback
            
        # Add a pill/badge behind the text so it looks perfect on any background
        self.text_badge = ctk.CTkFrame(self.left_panel, fg_color=("#ffffff", "#1e1e1e"), corner_radius=20, border_width=1, border_color=("#e2e8f0", "#333"))
        self.text_badge.place(relx=0.5, rely=0.5, anchor="center")
        
        self.brand_label = ctk.CTkLabel(self.text_badge, text="Smart College", font=ctk.CTkFont(size=55, weight="bold"), text_color=("#0f172a", "white"))
        self.brand_label.pack(pady=(30, 5), padx=50)
        
        self.desc_label = ctk.CTkLabel(self.text_badge, text="Secure Authentication Portal", font=ctk.CTkFont(size=20), text_color=("#475569", "#cbd5e1"))
        self.desc_label.pack(pady=(0, 30), padx=50)

        # Right Panel
        self.right_panel = ctk.CTkFrame(self, fg_color=("#f8fafc", "#1a1a1a"), corner_radius=0)
        self.right_panel.grid(row=0, column=1, sticky="nsew")
        
        # New Interactive Theme Button
        self.theme_btn = ctk.CTkButton(self.right_panel, text="Theme: 🌙", command=self.toggle_theme, font=ctk.CTkFont(size=14, weight="bold"), cursor="hand2", fg_color=("#e2e8f0", "#2b2b2b"), text_color=("#0f172a", "white"), hover_color=("#cbd5e1", "#3d3d3d"), width=120, corner_radius=20)
        self.theme_btn.place(relx=0.95, rely=0.05, anchor="ne")
        
        self.form_frame = ctk.CTkFrame(self.right_panel, width=420, height=520, corner_radius=20, fg_color=("#ffffff", "#242424"), border_width=1, border_color=("#e2e8f0", "#333"))
        self.form_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.is_login = True
        
        self.title_label = ctk.CTkLabel(self.form_frame, text="Welcome Back", font=ctk.CTkFont(size=36, weight="bold"), text_color=("#0f172a", "white"))
        self.title_label.grid(row=0, column=0, pady=(50, 40), padx=50)
        
        self.username_entry = ctk.CTkEntry(self.form_frame, width=300, height=50, placeholder_text="Username", font=ctk.CTkFont(size=16), border_width=2, corner_radius=10, fg_color=("#f1f5f9", "#333333"), border_color=("#cbd5e1", "#444"))
        self.username_entry.grid(row=1, column=0, pady=(0, 20), padx=50)
        self.username_entry.bind("<FocusIn>", lambda e: self.username_entry.configure(border_color="#3b82f6"))
        self.username_entry.bind("<FocusOut>", lambda e: self.username_entry.configure(border_color=("#cbd5e1", "#444")))
        
        self.password_entry = ctk.CTkEntry(self.form_frame, width=300, height=50, placeholder_text="Password", show="*", font=ctk.CTkFont(size=16), border_width=2, corner_radius=10, fg_color=("#f1f5f9", "#333333"), border_color=("#cbd5e1", "#444"))
        self.password_entry.grid(row=2, column=0, pady=(0, 30), padx=50)
        self.password_entry.bind("<FocusIn>", lambda e: self.password_entry.configure(border_color="#3b82f6"))
        self.password_entry.bind("<FocusOut>", lambda e: self.password_entry.configure(border_color=("#cbd5e1", "#444")))
        
        self.action_button = ctk.CTkButton(self.form_frame, text="Secure Login", width=300, height=50, font=ctk.CTkFont(weight="bold", size=18), corner_radius=10, command=self.handle_action, cursor="hand2")
        self.action_button.grid(row=3, column=0, pady=(0, 20), padx=50)
        
        self.action_button.bind("<Enter>", lambda e: self.action_button.configure(fg_color="#2563eb"))
        self.action_button.bind("<Leave>", lambda e: self.action_button.configure(fg_color="#1f6aa5"))
        
        self.toggle_button = ctk.CTkButton(self.form_frame, text="Don't have an account? Sign up", fg_color="transparent", text_color=("#475569", "gray"), hover_color=("#e2e8f0", "#2b2b2b"), font=ctk.CTkFont(size=14, underline=True), command=self.toggle_mode, cursor="hand2")
        self.toggle_button.grid(row=4, column=0, pady=(0, 30), padx=50)

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme_btn.configure(text="Theme: ☀️")
        else:
            ctk.set_appearance_mode("Dark")
            self.theme_btn.configure(text="Theme: 🌙")

    def toggle_mode(self):
        self.is_login = not self.is_login
        if self.is_login:
            self.title_label.configure(text="Welcome Back")
            self.action_button.configure(text="Secure Login")
            self.toggle_button.configure(text="Don't have an account? Sign up")
        else:
            self.title_label.configure(text="Create Account")
            self.action_button.configure(text="Sign Up")
            self.toggle_button.configure(text="Already have an account? Login")
            
    def handle_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            with open(self.users_file, "r") as f:
                users = json.load(f)
        except Exception:
            users = {}
            
        if self.is_login:
            if username in users and users[username] == password:
                self.destroy() 
                subprocess.Popen(["python", "attendance.py", "--dashboard"])
            else:
                messagebox.showerror("Error", "Invalid username or password")
        else:
            if username in users:
                messagebox.showerror("Error", "Username already exists")
            else:
                users[username] = password
                with open(self.users_file, "w") as f:
                    json.dump(users, f)
                messagebox.showinfo("Success", "Account created successfully! You can now login.")
                self.toggle_mode()

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
