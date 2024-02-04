#!/usr/bin/env python3

import tkinter as tk
from tkinter import messagebox
import webbrowser
import logging
import traceback
import os
import sys

# Configure the basic settings for logging
logging.basicConfig(filename="grade_calculator.log", level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Create a logger object
logger = logging.getLogger(__name__)

num_assignments = 0
assignment_grades = []  
assignment_totals = []

def ordinal(n):
    return "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])

html_link = "https://freetutoringcenter.com/"  

def center_window(window):
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

def open_link():
    try:
        webbrowser.open(html_link)
        logger.info(f"Opened the link: {html_link}")
        root.quit()  # Close the application
    except Exception as e:
        show_error_and_restart(f"Could not open the link: {e}")

def show_error_and_restart(message):
    error_window = tk.Toplevel(root)
    error_window.geometry("300x100")
    center_window(error_window)
    error_window.configure(bg='yellow')  # Set the background color to yellow
    error_label = tk.Label(error_window, text=message, fg='dark red', bg='yellow', font=("Helvetica", 11, "bold"))
    error_label.pack(pady=10)

    def restart_program():
        python = sys.executable
        os.execl(python, python, * sys.argv)

    okay_button = tk.Button(error_window, text="Okay", command=restart_program, bg='orange', font=("Helvetica", 11, "bold"))
    okay_button.pack(pady=10)

def calculate_grade():
    global num_assignments
    try:
        num_assignments = int(num_assignments_entry.get())
        if num_assignments < 0:
            raise ValueError("Number of assignments must be non-negative.")
        logger.info(f"Got the number of assignments: {num_assignments}")
    except ValueError as e:
        show_error_and_restart(f"Invalid input: {e}")
        return
    for i in range(0, num_assignments, 1):
        total_window = tk.Toplevel(root)
        total_window.geometry("450x50")
        total_window.configure(bg='yellow')  # Set the background color to yellow
        center_window(total_window)
        total_text = tk.Entry(total_window, width=50, font=("Helvetica", 11, "bold"), bg='yellow')
        total_text.pack()
        total_text.insert(0, f'Points possible for the {ordinal(i + 1)} assignment')
 
        def submit_total(event=None):
            try:
                total = int(total_text.get())
                if total < 0:
                    raise ValueError("Total must be non-negative.")
                assignment_totals.append(total)
                total_window.destroy()
                logger.info(f"Got the total for assignment {i+1}: {total}")
            except ValueError as e:
                show_error_and_restart(f"Invalid input: {e}")

        def clear_text(event):
            total_text.delete(0,'end')

        total_text.bind('<FocusIn>', clear_text)  # Clear text when the widget is clicked
        total_text.bind('<Return>', submit_total)  # Submit total when Enter is pressed

        submit_button = tk.Button(total_window, text="Submit Total", command=submit_total, bg='orange', font=("Helvetica", 11, "bold"))
        submit_button.pack()
        total_window.wait_window()  

        grade_window = tk.Toplevel(root)
        grade_window.geometry("450x50")
        grade_window.configure(bg='yellow')  # Set the background color to yellow
        center_window(grade_window)
        grade_text = tk.Entry(grade_window, width=50, font=("Helvetica", 11, "bold"), bg='yellow')
        grade_text.pack()
        grade_text.insert(0, f'Grade received on the {ordinal(1 + i)} assignment')

        def submit_grade(event=None):
            try:
                grade = int(grade_text.get())
                if grade < 0:
                    raise ValueError("Grade must be non-negative.")
                if grade > assignment_totals[i]:
                    raise ValueError("Grade cannot be greater than total.")
                assignment_grades.append(grade)
                grade_window.destroy()
                logger.info(f"Got the grade for assignment {i+1}: {grade}")
            except ValueError as e:
                show_error_and_restart(f"Invalid input: {e}")

        def clear_grade_text(event):
            grade_text.delete(0,'end')

        grade_text.bind('<FocusIn>', clear_grade_text)  # Clear text when the widget is clicked
        grade_text.bind('<Return>', submit_grade)  # Submit grade when Enter is pressed

        submit_button = tk.Button(grade_window, text="Submit Grade", command=submit_grade, bg='orange', font=("Helvetica", 11, "bold"))
        submit_button.pack()
        grade_window.wait_window()

    try:
        assignment_totals_received = sum(assignment_grades)
        assignment_totals_possible = sum(assignment_totals)
        if assignment_totals_possible != 0:
            assignment_percent = (assignment_totals_received / assignment_totals_possible) * 100
        else:
            raise ZeroDivisionError("No assignments completed.")
        logger.info(f"Calculated the grade percentage: {assignment_percent}")
    except ZeroDivisionError as e:
        show_error_and_restart(f"Could not calculate grade: {e}")
        return

    result_window = tk.Toplevel(root)
    result_window.geometry("650x300")  # Increased the width by 50 pixels
    result_window.configure(bg='yellow')  # Set the background color to yellow
    center_window(result_window)
    result_label = tk.Label(result_window, text='You have completed {:.0f} so far in this course.\nThe total points received on the {:.0f} assignments is {:.0f} points, out of the {:.0f} points possible.'.format(num_assignments, num_assignments, assignment_totals_received, assignment_totals_possible), fg='dark red', bg='yellow', font=("Helvetica", 11, "bold"))
    result_label.pack(pady=10)

    if assignment_percent >= 90 and assignment_percent < 100:
        result_text = f"The grade you received was a {assignment_percent}%, so far. You should be happy to get an A. If you seek further seek further knowledge visit {html_link}."
    elif assignment_percent >= 80 and assignment_percent < 90:
        result_text = f"The grade you received so far in the course was a {assignment_percent}%. You should be happy with a B; however, if not review this website {html_link}."
    elif assignment_percent >= 70 and assignment_percent < 80:
        result_text = f'The grade received so far in the class was a {assignment_percent}%. You should raise your C by visiting {html_link}.'
    elif assignment_percent >= 60 and assignment_percent < 70:
        result_text = f'Your current grade is {assignment_percent}%, which is a D. You can raise your grade by visiting {html_link}.'
    else:
        result_text = f'You got an F with a low grade of {assignment_percent}%. You should immediately visit {html_link} and start to study.'

    result_message = tk.Message(result_window, text=result_text, fg='dark red', bg='yellow', font=("Helvetica", 11, "bold"))
    result_message.pack(pady=10)

    open_link_button = tk.Button(result_window, text="Open Link", command=open_link, bg='orange', font=("Helvetica", 11, "bold"))
    open_link_button.pack(pady=10)

root = tk.Tk()
root.geometry("800x800")
root.configure(bg='yellow')  # Set the background color to yellow
center_window(root)

num_assignments_label = tk.Label(root, text="How many assignments have been completed in the class so far?", fg='dark red', bg='yellow', font=("Helvetica", 11, "bold"))
num_assignments_label.pack()

num_assignments_entry = tk.Entry(root, fg='dark red', bg='yellow', font=("Helvetica", 11, "bold"))
num_assignments_entry.pack()

calculate_button = tk.Button(root, text="Calculate Grade", command=calculate_grade, bg='orange', font=("Helvetica", 11, "bold"))
calculate_button.pack()

assignment_grades.clear()
assignment_totals.clear()
num_assignments = 0

root.mainloop()
