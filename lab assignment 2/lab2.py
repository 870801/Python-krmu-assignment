"""
GradeBook Analyzer
Author: <YOUR NAME>
Date: 25 Nov 2025
Description: CLI tool for reading student marks, analysing statistics,
assigning grades, and printing formatted reports.
"""

import csv
import statistics

# --------------------------------------------------------
# Task 3 — Statistical Functions
# --------------------------------------------------------

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    max_student = max(marks_dict, key=marks_dict.get)
    return max_student, marks_dict[max_student]

def find_min_score(marks_dict):
    min_student = min(marks_dict, key=marks_dict.get)
    return min_student, marks_dict[min_student]


# --------------------------------------------------------
# Task 4 — Grade Assignment
# --------------------------------------------------------

def assign_grades(marks_dict):
    grades = {}

    for name, score in marks_dict.items():
        if score >= 90:
            grades[name] = "A"
        elif score >= 80:
            grades[name] = "B"
        elif score >= 70:
            grades[name] = "C"
        elif score >= 60:
            grades[name] = "D"
        else:
            grades[name] = "F"

    return grades


def grade_distribution(grades_dict):
    counts = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
    for g in grades_dict.values():
        counts[g] += 1
    return counts


# --------------------------------------------------------
# Task 2 — Data Entry & CSV Loading
# --------------------------------------------------------

def manual_input():
    marks = {}
    n = int(input("\nEnter number of students: "))

    for _ in range(n):
        name = input("Enter student name: ")
        score = int(input("Enter marks: "))
        marks[name] = score

    return marks


def load_csv():
    file_path = input("\nEnter CSV file path: ")
    marks = {}

    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                name = row[0]
                score = int(row[1])
                marks[name] = score
        print("CSV loaded successfully!")
    except Exception as e:
        print("Error loading CSV:", e)

    return marks


# --------------------------------------------------------
# Task 6 — Output Table
# --------------------------------------------------------

def print_results_table(marks, grades):
    print("\nName\t\tMarks\tGrade")
    print("--------------------------------------")

    for name in marks:
        print(f"{name:12}\t{marks[name]}\t{grades[name]}")

    print("--------------------------------------\n")


# --------------------------------------------------------
# Task 5 – Pass/Fail using list comprehension
# --------------------------------------------------------

def pass_fail_lists(marks_dict):
    passed = [name for name, m in marks_dict.items() if m >= 40]
    failed = [name for name, m in marks_dict.items() if m < 40]
    return passed, failed


# --------------------------------------------------------
# CLI LOOP (Task 1 + Task 6)
# --------------------------------------------------------

def main():
    print("\n===== Welcome to GradeBook Analyzer =====")
    print("A Python tool for analysing student marks.\n")

    while True:
        print("\nChoose input method:")
        print("1. Manual data entry")
        print("2. Load CSV file")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            marks = manual_input()
        elif choice == "2":
            marks = load_csv()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
            continue

        if not marks:
            print("No data found. Try again.")
            continue

        # Statistical analysis
        avg = calculate_average(marks)
        med = calculate_median(marks)
        max_name, max_score = find_max_score(marks)
        min_name, min_score = find_min_score(marks)

        # Grade assignment
        grades = assign_grades(marks)
        dist = grade_distribution(grades)

        # Pass/Fail
        passed, failed = pass_fail_lists(marks)

        # Print summary
        print("\n===== ANALYSIS SUMMARY =====")
        print(f"Average Score: {avg:.2f}")
        print(f"Median Score: {med}")
        print(f"Highest Score: {max_name} ({max_score})")
        print(f"Lowest Score:  {min_name} ({min_score})")

        print("\nGrade Distribution:")
        for g, c in dist.items():
            print(f"{g}: {c}")

        print("\nPassed Students:", passed)
        print("Failed Students:", failed)

        # Print formatted table
        print_results_table(marks, grades)

        # Repeat?
        again = input("Run analysis again? (y/n): ").lower()
        if again != "y":
            print("Thank you for using GradeBook Analyzer!")
            break


# Run program
if __name__ == "__main__":
    main()

import csv
 def read_csv().
    with open ("CSV FILE.PY")



 