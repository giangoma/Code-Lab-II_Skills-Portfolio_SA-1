import tkinter as tk
from tkinter import Frame, Label, Button, Entry, Listbox, Scrollbar, END, messagebox, simpledialog
from PIL import Image, ImageTk

class StudentManager:
    def __init__(self, filename):
        self.filename = filename
        self.students = self.load_students()
        self.init_gui()

    # Loads student data from file
    def load_students(self):
        students = []
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                num_students = int(lines[0])
                for line in lines[1:num_students + 1]:
                    parts = line.strip().split(',')
                    try:
                        student = {
                            'code': parts[0],
                            'name': parts[1],
                            'coursework': [int(x) if x.isdigit() else 0 for x in parts[2:5]],
                            'exam': int(parts[5]) if parts[5].isdigit() else 0
                        }
                        students.append(student)
                    except ValueError as e:
                        print(f"There was an error in parsing student data: {e}")
        except Exception as e:
            print(f"There was an error loading students: {e}")
        return students

    # Saves student data to file
    def save_students(self):
        with open(self.filename, 'w') as file:
            file.write(f"{len(self.students)}\n")
            for student in self.students:
                file.write(f"{student['code']},{student['name']},{','.join(map(str, student['coursework']))},{student['exam']}\n")

    # Calculates total coursework mark for a student
    def get_total_coursework_mark(self, student):
        return sum(student['coursework'])

    # Calculates overall percentage for a student
    def get_overall_percentage(self, student):
        total_marks = self.get_total_coursework_mark(student) + student['exam']
        return (total_marks / 160) * 100

    # Determines the grade based on percentage
    def get_grade(self, percentage):
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'

    # Displays all student records in the listbox
    def view_all_students(self):
        self.listbox.delete(0, END)
        for student in self.students:
            self.listbox.insert(END, self.format_student_record(student))
        self.print_summary()

    # View a specific student's record
    def view_individual_student(self):
        search = self.entry_search.get().strip()
        for student in self.students:
            if search.lower() in student['name'].lower() or search == student['code']:
                self.listbox.delete(0, END)
                self.listbox.insert(END, self.format_student_record(student))
                return
        messagebox.showerror("Error", "Student not found!")

    # Format student's record for display
    def format_student_record(self, student):
        total_coursework = self.get_total_coursework_mark(student)
        percentage = self.get_overall_percentage(student)
        grade = self.get_grade(percentage)
        return (f"Name: {student['name']}, Number: {student['code']}, "
                f"Total Coursework: {total_coursework}, Exam Mark: {student['exam']}, "
                f"Overall %: {percentage:.2f}, Grade: {grade}")

    # Print summary of all students
    def print_summary(self):
        num_students = len(self.students)
        total_percentage = sum(self.get_overall_percentage(s) for s in self.students)
        average_percentage = total_percentage / num_students
        summary = f"Number of students: {num_students}, Average percentage: {average_percentage:.2f}"
        self.listbox.insert(END, summary)

    # Show the student with the highest/lowest percentage
    def show_highest_lowest(self, high=True):
        best_student = max(self.students, key=self.get_overall_percentage) if high else min(self.students, key=self.get_overall_percentage)
        self.listbox.delete(0, END)
        self.listbox.insert(END, self.format_student_record(best_student))

    # Sort students by overall percentage
    def sort_students(self, ascending=True):
        self.students.sort(key=self.get_overall_percentage, reverse=not ascending)
        self.view_all_students()

    # Adds new student
    def add_student(self):
        code = simpledialog.askstring("Input", "Enter student code:")
        if code is None:
            return
        name = simpledialog.askstring("Input", "Enter student name:")
        if name is None:
            return
        coursework = []
        for i in range(3):
            mark = simpledialog.askinteger("Input", f"Enter coursework mark {i+1} (0-20):")
            if mark is None:
                return
            coursework.append(mark)
        exam = simpledialog.askinteger("Input", "Enter exam mark (0-100):")
        if exam is None:
            return

        new_student = {
            'code': code,
            'name': name,
            'coursework': coursework,
            'exam': exam
        }
        self.students.append(new_student)
        self.save_students()
        messagebox.showinfo("Success", "Student record added successfully.")

    # Deletes student from record
    def delete_student(self):
        search = self.entry_search.get().strip()
        if not search:
            messagebox.showerror("Error", "Please enter a student code or name to search.")
            return
        for i, student in enumerate(self.students):
            if search.lower() in student['name'].lower() or search == student['code']:
                if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the record for {student['name']}?"):
                    del self.students[i]
                    self.save_students()
                    messagebox.showinfo("Success", "The student record has been deleted successfully.")
                else:
                    messagebox.showinfo("Canceled", "The student record deletion has been canceled.")
                return
        messagebox.showerror("Error", "Student not found!")

    # Update student's details
    def update_student(self):
        search = self.entry_search.get().strip()
        for student in self.students:
            if search.lower() in student['name'].lower() or search == student['code']:
                student['name'] = simpledialog.askstring("Input", "Enter new name:", initialvalue=student['name'])
                student['coursework'] = [simpledialog.askinteger("Input", f"Enter new coursework mark {i+1} (0-20):", initialvalue=student['coursework'][i]) for i in range(3)]
                student['exam'] = simpledialog.askinteger("Input", "Enter new exam mark (0-100):", initialvalue=student['exam'])
                self.save_students()
                messagebox.showinfo("Success", "Student record updated successfully.")
                return
        messagebox.showerror("Error", "Student not found!")

    # Initialize the GUI
    def init_gui(self):
        self.root = tk.Tk()
        self.root.title("Student Manager")
        self.root.geometry("700x500")
        self.root.resizable(False, False)

        # Set background image
        self.background_image = Image.open('C:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Student Manager/Assets/background.jpg')
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        frame_output = Frame(self.root)
        frame_output.place(x=250, y=120, width=420, height=350)

        # Listbox to display students
        self.listbox = Listbox(frame_output, width=80, height=25, font=("Roboto", 10))
        self.listbox.pack(side="left", fill="y")

        # Scrollbar for the listbox
        scrollbar = Scrollbar(frame_output, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        frame_buttons = Frame(self.root, bg="#22263c")
        frame_buttons.place(x=30, y=250, width=200, height=250)

        # Buttons for all necessary functions seen in the GUI
        buttons = [
            ("View All", self.view_all_students),
            ("Highest", lambda: self.show_highest_lowest(True)),
            ("Lowest", lambda: self.show_highest_lowest(False)),
            ("Sort Asc", lambda: self.sort_students(True)),
            ("Sort Desc", lambda: self.sort_students(False)),
            ("Add", self.add_student),
            ("Delete", self.delete_student),
            ("Update", self.update_student),
        ]

        for i, (text, command) in enumerate(buttons):
            row, col = divmod(i, 2)
            button = Button(frame_buttons, text=text, command=command, width=10, font=("Roboto", 10))
            button.grid(row=row, column=col, padx=10, pady=5)

        frame_search = Frame(self.root, bg="#22263c")
        frame_search.place(x=30, y=430, width=200, height=50)

        # Entry and button for searching a student
        self.entry_search = Entry(frame_search, width=20, bg="lightgray", font=("Roboto", 10))
        self.entry_search.pack(side="left", padx=5)
        btn_search = Button(frame_search, text="🔍", command=self.view_individual_student, font=("Roboto", 10))  
        btn_search.pack(side="left", padx=5)

        self.root.mainloop()

if __name__ == "__main__":
    manager = StudentManager('C:/Users/giang/Documents/GitHub/skills-portfolio-giangoma/A1 - Skills Portfolio/Student Manager/Assets/studentMarks.txt')
    manager.init_gui()

#Resources used: 
#> All other visual resources were made in Canva. www.canva.com