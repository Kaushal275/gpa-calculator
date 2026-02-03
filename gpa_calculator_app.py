def calculate_percentage(marks_obtained, full_marks):
    """Calculate percentage correctly"""
    return (marks_obtained / full_marks) * 100


def assign_grade(percentage):
    """Assign grade and grade point based on fixed bands"""
    for grade_row in GRADE_TABLE:
        if grade_row["min"] <= percentage <= grade_row["max"]:
            return grade_row["grade"], grade_row["point"]
    return "F", 0.0


def calculate_weighted_point(grade_point, credit):
    """Grade point weighted by component credit"""
    return grade_point * credit


def calculate_semester_gpa(marks_data, semester_name):
    """
    Correct GPA calculation:
    - Theory and Practical counted separately
    - Zero marks treated as valid (F grade)
    - All credits included
    """
    total_weighted_points = 0.0
    total_credits = 0.0

    curriculum = CIVIL_ENGINEERING_CURRICULUM[semester_name]

    for subject in curriculum:
        credit = subject["credit"]
        key = f"{subject['code']}_{subject['type']}"

        # Skip only if credit is zero (non-GPA components)
        if credit <= 0:
            continue

        # If marks not entered, skip (exam not taken yet)
        if key not in marks_data:
            continue

        marks = marks_data[key]

        # Zero marks are VALID
        percentage = calculate_percentage(marks, subject["full_marks"])
        grade, grade_point = assign_grade(percentage)

        weighted_point = calculate_weighted_point(grade_point, credit)

        total_weighted_points += weighted_point
        total_credits += credit

    if total_credits == 0:
        return 0.0, 0.0, 0.0

    gpa = total_weighted_points / total_credits
    return round(gpa, 2), total_weighted_points, total_credits


def calculate_cumulative_gpa(all_semester_marks):
    """Correct cumulative GPA across semesters"""
    total_weighted_points = 0.0
    total_credits = 0.0

    for semester_name, marks_data in all_semester_marks.items():
        curriculum = CIVIL_ENGINEERING_CURRICULUM[semester_name]

        for subject in curriculum:
            credit = subject["credit"]
            key = f"{subject['code']}_{subject['type']}"

            if credit <= 0 or key not in marks_data:
                continue

            marks = marks_data[key]
            percentage = calculate_percentage(marks, subject["full_marks"])
            _, grade_point = assign_grade(percentage)

            total_weighted_points += grade_point * credit
            total_credits += credit

    if total_credits == 0:
        return 0.0, 0.0, 0.0

    cgpa = total_weighted_points / total_credits
    return round(cgpa, 2), total_weighted_points, total_credits
