import tkinter as tk
from tkinter import messagebox
from typing import List

num_assignments = 0
assignment_grades: List[int] = []
assignment_totals: List[int] = []


def ordinal(n: int) -> str:
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4])


html_link = "https://varsitytutoring.com/"


def calculate_grade():
    global num_assignments
    num_assignments = int(num_assignments_entry.get())
    for i in range(0, num_assignments, 1):
        total_window = tk.Toplevel(root)
        total_window.geometry("450x50")
        total_text = tk.Entry(total_window, width=50)
        total_text.pack()
        total_text.insert(0, f"Points possible for the {ordinal(i + 1)} assignment")

        def submit_total(event=None):
            total = int(total_text.get())
            if total < 0:
                raise ValueError("Total must be non-negative.")
            assignment_totals.append(total)
            total_window.destroy()

        def clear_text(event):
            total_text.delete(0, "end")

        total_text.bind(
            "<FocusIn>", clear_text
        )  # Clear text when the widget is clicked
        total_text.bind("<Return>", submit_total)  # Submit total when Enter is pressed

        submit_button = tk.Button(
            total_window, text="Submit Total", command=submit_total
        )
        submit_button.pack()
        total_window.wait_window()

        grade_window = tk.Toplevel(root)
        grade_window.geometry("450x50")
        grade_text = tk.Entry(grade_window, width=50)
        grade_text.pack()
        grade_text.insert(0, f"Grade received on the {ordinal(1 + i)} assignment")

        def submit_grade(event=None):
            grade = int(grade_text.get())
            if grade < 0:
                raise ValueError("Grade must be non-negative.")
            if grade > assignment_totals[i]:
                raise ValueError("Grade cannot be greater than total.")
            assignment_grades.append(grade)
            grade_window.destroy()

        def clear_grade_text(event):
            grade_text.delete(0, "end")

        grade_text.bind(
            "<FocusIn>", clear_grade_text
        )  # Clear text when the widget is clicked
        grade_text.bind("<Return>", submit_grade)  # Submit grade when Enter is pressed

        submit_button = tk.Button(
            grade_window, text="Submit Grade", command=submit_grade
        )
        submit_button.pack()
        grade_window.wait_window()

    assignment_totals_received = sum(assignment_grades)
    assignment_totals_possible = sum(assignment_totals)
    if assignment_totals_possible != 0:
        assignment_percent = (
            assignment_totals_received / assignment_totals_possible
        ) * 100
    else:
        assignment_percent = 0

    messagebox.showinfo(
        "Results",
        "You have completed {:.0f} so far in this course.\nThe total points received on the {:.0f} assignments is {:.0f} points, out of the {:.0f} points possible.".format(
            num_assignments,
            num_assignments,
            assignment_totals_received,
            assignment_totals_possible,
        ),
    )

    if assignment_percent > 90 and assignment_percent <= 100:
        messagebox.showinfo(
            "Result",
            f"The grade you received was a {assignment_percent}% so far. You should be happy with an A; however, if not visit {html_link}.",
        )
    elif assignment_percent > 80 and assignment_percent <= 90:
        messagebox.showinfo(
            "Results",
            f"The grade you received so far in the course was a {assignment_percent}%. You should be happy with a B; however, if not review this website {html_link}.",
        )
    elif assignment_percent > 70 and assignment_percent <= 80:
        messagebox.showinfo(
            "Results",
            f"The grade received so far in the class was a {assignment_percent}%. You should raise your C by visiting {html_link}.",
        )
    elif assignment_percent > 60 and assignment_percent <= 70:
        messagebox.showinfo(
            "Results",
            f"Your current grade is {assignment_percent}%, which is a D. You can raise your grade by visiting {html_link}.",
        )
    else:
        messagebox.showinfo(
            "Results",
            f"You got an F with a low grade of {assignment_percent}%. You should immediatly visit {html_link} and start to study.",
        )


root = tk.Tk()
root.geometry("800x800")

num_assignments_label = tk.Label(
    root, text="How many assignments have been completed in the class so far?"
)
num_assignments_label.pack()

num_assignments_entry = tk.Entry(root)
num_assignments_entry.pack()

calculate_button = tk.Button(root, text="Calculate Grade", command=calculate_grade)
calculate_button.pack()

root.mainloop()
