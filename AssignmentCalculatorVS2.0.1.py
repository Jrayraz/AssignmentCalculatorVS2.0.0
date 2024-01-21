import tkinter as tk
from tkinter import messagebox
import webbrowser

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
    webbrowser.open(html_link)

def calculate_grade():
    global num_assignments
    num_assignments = int(num_assignments_entry.get())
    for i in range(0, num_assignments, 1):
        total_window = tk.Toplevel(root)
        total_window.geometry("450x50")
        center_window(total_window)
        total_text = tk.Entry(total_window, width=50)
        total_text.pack()
        total_text.insert(0, f'Points possible for the {ordinal(i + 1)} assignment')

        def submit_total(event=None):
            total = int(total_text.get())
            if total < 0:
                raise ValueError("Total must be non-negative.")
            assignment_totals.append(total)
            total_window.destroy()

        def clear_text(event):
            total_text.delete(0,'end')

        total_text.bind('<FocusIn>', clear_text)  # Clear text when the widget is clicked
        total_text.bind('<Return>', submit_total)  # Submit total when Enter is pressed

        submit_button = tk.Button(total_window, text="Submit Total", command=submit_total)
        submit_button.pack()
        total_window.wait_window()  

        grade_window = tk.Toplevel(root)
        grade_window.geometry("450x50")
        center_window(grade_window)
        grade_text = tk.Entry(grade_window, width=50)
        grade_text.pack()
        grade_text.insert(0, f'Grade received on the {ordinal(1 + i)} assignment')

        def submit_grade(event=None):
            grade = int(grade_text.get())
            if grade < 0:
                raise ValueError("Grade must be non-negative.")
            if grade > assignment_totals[i]:
                raise ValueError("Grade cannot be greater than total.")
            assignment_grades.append(grade)
            grade_window.destroy()

        def clear_grade_text(event):
            grade_text.delete(0,'end')

        grade_text.bind('<FocusIn>', clear_grade_text)  # Clear text when the widget is clicked
        grade_text.bind('<Return>', submit_grade)  # Submit grade when Enter is pressed

        submit_button = tk.Button(grade_window, text="Submit Grade", command=submit_grade)
        submit_button.pack()
        grade_window.wait_window()

    assignment_totals_received = sum(assignment_grades)
    assignment_totals_possible = sum(assignment_totals)
    if assignment_totals_possible != 0:
        assignment_percent = (assignment_totals_received / assignment_totals_possible) * 100
    else:
        assignment_percent = 0

    result_window = tk.Toplevel(root)
    result_window.geometry("600x300")
    center_window(result_window)
    result_label = tk.Label(result_window, text='You have completed {:.0f} so far in this course.\nThe total points received on the {:.0f} assignments is {:.0f} points, out of the {:.0f} points possible.'.format(num_assignments, num_assignments, assignment_totals_received, assignment_totals_possible))
    result_label.pack(pady=10)

    if assignment_percent > 90 and assignment_percent <= 100:
        result_text = f"The grade you received was a {assignment_percent}% so far. You should be happy with an A; however, if not visit {html_link}."
    elif assignment_percent > 80 and assignment_percent <= 90:
        result_text = f"The grade you received so far in the course was a {assignment_percent}%. You should be happy with a B; however, if not review this website {html_link}."
    elif assignment_percent > 70 and assignment_percent <= 80:
        result_text = f'The grade received so far in the class was a {assignment_percent}%. You should raise your C by visiting {html_link}.'
    elif assignment_percent > 60 and assignment_percent <= 70:
        result_text = f'Your current grade is {assignment_percent}%, which is a D. You can raise your grade by visiting {html_link}.'
    else:
        result_text = f'You got an F with a low grade of {assignment_percent}%. You should immediately visit {html_link} and start to study.'

    result_message = tk.Message(result_window, text=result_text)
    result_message.pack(pady=10)

    open_link_button = tk.Button(result_window, text="Open Link", command=open_link)
    open_link_button.pack(pady=10)

root = tk.Tk()
root.geometry("800x800")
center_window(root)

num_assignments_label = tk.Label(root, text="How many assignments have been completed in the class so far?")
num_assignments_label.pack()

num_assignments_entry = tk.Entry(root)
num_assignments_entry.pack()

calculate_button = tk.Button(root, text="Calculate Grade", command=calculate_grade)
calculate_button.pack()

root.mainloop()

