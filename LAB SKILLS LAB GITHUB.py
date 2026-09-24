"""
Lab Experiment: Student Grade Management & Performance Analyzer
Author: [Your Name]
Description: A robust Python program demonstrating OOP, file handling, 
             and data processing to track and analyze student grades.
"""

import json
import os

class Student:
    def __init__(self, student_id: str, name: str, scores: list):
        self.student_id = student_id
        self.name = name
        self.scores = scores

    def calculate_average(self) -> float:
        """Calculates the average score, handles empty lists gracefully."""
        if not self.scores:
            return 0.0
        return round(sum(self.scores) / len(self.scores), 2)

    def get_final_grade(self) -> str:
        """Determines the letter grade based on the average score."""
        avg = self.calculate_average()
        if avg >= 90: return 'A'
        elif avg >= 80: return 'B'
        elif avg >= 70: return 'C'
        elif avg >= 60: return 'D'
        else: return 'F'

    def to_dict(self) -> dict:
        """Converts object details to a dictionary for JSON storage."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "scores": self.scores,
            "average": self.calculate_average(),
            "final_grade": self.get_final_grade()
        }


class LabGradeBook:
    def __init__(self, filename="lab_records.json"):
        self.filename = filename
        self.students = {}
        self.load_records()

    def add_student(self, student_id: str, name: str, scores: list):
        """Adds or updates a student in the registry."""
        if not student_id or not name:
            raise ValueError("Student ID and Name cannot be empty!")
        
        self.students[student_id] = Student(student_id, name, scores)
        print(f"Successfully added/updated record for: {name}")

    def save_records(self):
        """Saves current laboratory data out to a JSON file."""
        data_to_save = {sid: s.to_dict() for sid, s in self.students.items()}
        with open(self.filename, 'w') as file:
            json.dump(data_to_save, file, indent=4)
        print(f"Records successfully backed up to '{self.filename}'!")

    def load_records(self):
        """Loads historical student database records if file exists."""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for sid, info in data.items():
                        self.students[sid] = Student(sid, info['name'], info['scores'])
            except json.JSONDecodeError:
                print("Warning: Existing record file was corrupted. Starting fresh.")

    def display_report(self):
        """Prints a beautifully formatted dashboard directly to console."""
        if not self.students:
            print("\n--- No Student Records Found ---")
            return

        print("\n" + "="*65)
        print(f"{'ID':<10} | {'Student Name':<20} | {'Scores':<15} | {'Avg':<6} | {'Grade'}")
        print("="*65)
        for sid, s in self.students.items():
            scores_str = ", ".join(map(str, s.scores))
            print(f"{sid:<10} | {s.name:<20} | {scores_str:<15} | {s.calculate_average():<6} | {s.get_final_grade()}")
        print("="*65 + "\n")


# --- Execution Example ---
if __name__ == "__main__":
    print("Initializing Laboratory Gradebook System...")
    gradebook = LabGradeBook()

    # Seeding demo data
    try:
        gradebook.add_student("S101", "Alice Smith", [85, 92, 88])
        gradebook.add_student("S102", "Bob Jones", [70, 64, 78])
        gradebook.add_student("S103", "Charlie Brown", [95, 100, 98])
        
        # Display the loaded grades formatted cleanly 
        gradebook.display_report()
        
        # Persist information local data 
        gradebook.save_records()
        
    except ValueError as e:
        print(f"Error executing lab program: {e}")
