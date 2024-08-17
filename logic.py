import csv


def save_grades_to_csv(grades: list, filename: str = "grades.csv") -> None:
    """Save grades to CSV."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(grades)


def process_grades(grades: list) -> list:
    """Pad grades, calc average.

    Args:
        grades: List of student scores.

    Returns:
        List of grades with padding and average.
    """
    while len(grades) < 4:
        grades.append(0)

    non_zero_grades = []
    for grade in grades:
        if grade > 0:
            non_zero_grades.append(grade)

    if non_zero_grades:
        average_grade = sum(non_zero_grades) / len(non_zero_grades)
    else:
        average_grade = 0

    grades.append(average_grade)
    return grades
