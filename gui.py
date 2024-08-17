import tkinter as tk
from logic import save_grades_to_csv, process_grades


class InputField:
    def __init__(self, parent: tk.Widget, label_text: str, row: int, validate_func: callable):
        """Init input field with label and validation.

        Args:
            parent: Parent widget to contain this input field.
            label_text: Label text for the input field.
            row: Row in the grid where the input field will be placed.
            validate_func: Function for validating input.
        """
        self.label = tk.Label(parent, text=label_text, anchor='w')
        self.label.grid(row=row, column=0, padx=10, pady=5, sticky='w')
        self.entry = tk.Entry(parent)
        self.entry.grid(row=row, column=1, padx=10, pady=5, sticky='we')
        self.entry.bind('<KeyRelease>', validate_func)
        self.error_label = ErrorLabel(parent, row + 1)

    def get_value(self) -> str:
        """Return current input value.

        Returns:
            str: The current value of the input field.
        """
        return self.entry.get()

    def set_error(self, message: str) -> None:
        """Show error message.

        Args:
            message: Error message to display.
        """
        self.error_label.show(message)

    def clear_error(self) -> None:
        """Hide error message."""
        self.error_label.hide()


class ErrorLabel:
    def __init__(self, parent: tk.Widget, row: int):
        """Init error label.

        Args:
            parent: Parent widget to contain this error label.
            row: Row in the grid.
        """
        self.label = tk.Label(parent, text="", fg="red", anchor='w')
        self.label.grid(row=row, column=0, columnspan=2, padx=10, pady=2, sticky='w')
        self.hide()

    def show(self, message: str) -> None:
        """Display error.

        Args:
            message: Error message to display.
        """
        self.label.config(text=message)
        self.label.grid()

    def hide(self) -> None:
        """Hide error."""
        self.label.grid_remove()


def validate_inputs(event=None) -> bool:
    """Validate student count and scores.

    Args:
        event: The event that triggered validation, used in the binding.

    Returns:
        bool: True if all inputs are valid, otherwise False.
    """
    student_cnt = student_count_input.get_value()
    if not student_cnt.isdigit():
        student_count_input.set_error("Enter a number between 1 and 4.")
        btn_calculate.grid_remove()
        return False
    elif int(student_cnt) < 1 or int(student_cnt) > 4:
        student_count_input.set_error("Enter a number between 1 and 4.")
        btn_calculate.grid_remove()
        return False
    else:
        student_count_input.clear_error()

    all_filled = True
    for input_field in score_inputs:
        value = input_field.get_value()
        if value == "":
            all_filled = False
            input_field.clear_error()
        elif not value.isdigit():
            input_field.set_error("Enter only digits [0-9].")
            btn_calculate.grid_remove()
            return False
        elif int(value) < 0 or int(value) > 100:
            input_field.set_error("Enter a number between 0 and 100.")
            btn_calculate.grid_remove()
            return False
        else:
            input_field.clear_error()

    if all_filled:
        btn_calculate.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')
        return True
    else:
        btn_calculate.grid_remove()
        return False


def display_grades() -> None:
    """Process scores, calculates average, saves to the CSV, and display results."""
    if not validate_inputs():
        return

    student_cnt = int(student_count_input.get_value())
    scores = []
    for i in range(student_cnt):
        score = int(score_inputs[i].get_value())
        scores.append(score)

    processed_grades = process_grades(scores)
    save_grades_to_csv(processed_grades)

    display_message = ""
    for i, grade in enumerate(processed_grades[:-1]):
        display_message += f"Student {i + 1}: {grade}\n"
    display_message += f"Average: {processed_grades[-1]}"

    result_text.set(display_message)


def clear_score_entries() -> None:
    """Clear all score input fields."""
    for widget in score_frame.winfo_children():
        widget.destroy()
    score_inputs.clear()
    btn_calculate.grid_remove()


def create_score_entries(student_cnt: int) -> None:
    """Create score input fields based on student count.

    Args:
        student_cnt: Number of student score fields to create.
    """
    clear_score_entries()
    for i in range(student_cnt):
        score_input = InputField(score_frame, f"Student {i + 1} Score:", i * 2, validate_inputs)
        score_inputs.append(score_input)


def update_score_entries(event=None) -> None:
    """Update score input fields based on student count.

    Args:
        event: The event that triggered the update (optional).
    """
    student_cnt = student_count_input.get_value()

    student_count_input.clear_error()

    if not student_cnt.isdigit():
        student_count_input.set_error("Enter only digits [0-9].")
        clear_score_entries()
        return
    elif int(student_cnt) < 1 or int(student_cnt) > 4:
        student_count_input.set_error("Enter a number between 1 and 4.")
        clear_score_entries()
        return
    else:
        student_count_input.clear_error()
        student_cnt = int(student_cnt)
        create_score_entries(student_cnt)
        validate_inputs()


def create_widgets(root: tk.Tk) -> None:
    """Create main GUI widgets.

    Args:
        root: The root window of the Tkinter application.
    """
    global student_count_input, result_text, score_frame, btn_calculate, score_inputs

    score_inputs = []
    root.columnconfigure(1, weight=1)

    student_count_input = InputField(root, "Number of Students (1-4):", 0, update_score_entries)
    score_frame = tk.Frame(root)
    score_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky='we')

    result_text = tk.StringVar()
    result_label = tk.Label(root, textvariable=result_text, justify=tk.LEFT, anchor='w')
    result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='w')

    btn_calculate = tk.Button(root, text="Save Grades to CSV", command=display_grades)
    btn_calculate.grid_remove()


