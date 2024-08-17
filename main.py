import tkinter as tk
from gui import create_widgets

def main():
    # Create the main window
    root = tk.Tk()
    root.title("Student Grading System")
    root.geometry("400x300")
    root.resizable(True, True)
    create_widgets(root)
    root.mainloop()

if __name__ == "__main__":
    main()
