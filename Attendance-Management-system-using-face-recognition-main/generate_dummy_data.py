import os
import csv
import random
from datetime import datetime, timedelta

def generate_data():
    print("Generating 20+ LPA Tier Dummy Data...")

    # 1. Setup Student Details
    student_dir = "StudentDetails"
    os.makedirs(student_dir, exist_ok=True)
    student_file = os.path.join(student_dir, "studentdetails.csv")
    
    students = [
        (1001, "Priyanshi Yadav"),
        (1002, "Payal Sharma"),
        (1003, "Tushar Vishwakarma"),
        (1004, "Harsh Bajpai"),
        (1005, "Deepak Kushwaha"),
        (1006, "Anuruddh Yadav"),
        (1007, "Utkarsh Srivastav"),
        (1008, "Pranjal Pandey"),
        (1009, "Komal Kumari"),
        (1010, "Anshika Gupta")
    ]
    
    with open(student_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Enrollment", "Name"])
        writer.writerows(students)
    print(f"Generated {len(students)} students in {student_file}")

    # 2. Setup Attendance Logs for the last 7 days
    att_dir = "Attendance"
    os.makedirs(att_dir, exist_ok=True)
    
    today = datetime.now()
    
    for i in range(7):
        target_date = today - timedelta(days=6 - i) # Last 7 days, including today
        date_str = target_date.strftime("%Y-%m-%d")
        
        file_path = os.path.join(att_dir, f"Attendance_{date_str}.csv")
        
        # Randomly select who attended today (between 6 and 10 students)
        num_attended = random.randint(6, 10)
        attended_students = random.sample(students, num_attended)
        
        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Id", "Name", "Date", "Time"])
            for sid, sname in attended_students:
                # Randomize arrival time between 08:00 and 09:30
                hour = random.choice(["08", "09"])
                minute = str(random.randint(0, 59)).zfill(2)
                second = str(random.randint(0, 59)).zfill(2)
                time_str = f"{hour}:{minute}:{second}"
                
                writer.writerow([sid, sname, date_str, time_str])
        print(f"Generated {num_attended} attendance records for {date_str}")
        
    print("Dummy Data Generation Complete!")

if __name__ == "__main__":
    generate_data()
