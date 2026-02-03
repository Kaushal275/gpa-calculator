"""
GPA Calculator - Streamlit Application
Civil Engineering Program (Pre-populated Subjects)
Credit-Weighted, Grade-Based System
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="GPA Calculator - Civil Engineering",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== GRADE TABLE (FIXED, DISCRETE) ====================
GRADE_TABLE = [
    {"min": 80, "max": 100, "grade": "A", "point": 4.0},
    {"min": 75, "max": 79, "grade": "A−", "point": 3.7},
    {"min": 70, "max": 74, "grade": "B+", "point": 3.3},
    {"min": 65, "max": 69, "grade": "B", "point": 3.0},
    {"min": 60, "max": 64, "grade": "B−", "point": 2.7},
    {"min": 55, "max": 59, "grade": "C+", "point": 2.3},
    {"min": 50, "max": 54, "grade": "C", "point": 2.0},
    {"min": 0, "max": 49, "grade": "F", "point": 0.0}
]

# ==================== CIVIL ENGINEERING CURRICULUM ====================
CIVIL_ENGINEERING_CURRICULUM = {
    "Year 1 - Part I": [
        {"code": "SH 101", "name": "Engineering Mathematics I", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "SH 101", "name": "Engineering Mathematics I", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "SH 103", "name": "Engineering Chemistry", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "SH 103", "name": "Engineering Chemistry", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CT 101", "name": "Computer Programming", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CT 101", "name": "Computer Programming", "type": "P", "credit": 0, "full_marks": 50},
        {"code": "EE 103", "name": "Basic Electrical and Electronics Engineering", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "EE 103", "name": "Basic Electrical and Electronics Engineering", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 101", "name": "Engineering Mechanics", "type": "L+T", "credit": 4, "full_marks": 100},
        {"code": "CE 102", "name": "Engineering Geology I", "type": "L+T", "credit": 2, "full_marks": 75},
        {"code": "CE 102", "name": "Engineering Geology I", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 103", "name": "Civil Engineering Materials", "type": "L+T", "credit": 2, "full_marks": 50},
        {"code": "CE 103", "name": "Civil Engineering Materials", "type": "P", "credit": 0, "full_marks": 25},
    ],
    "Year 1 - Part II": [
        {"code": "SH 151", "name": "Engineering Mathematics II", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "SH 152", "name": "Engineering Physics", "type": "L+T", "credit": 4, "full_marks": 100},
        {"code": "SH 152", "name": "Engineering Physics", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "ME 158", "name": "Engineering Drawing", "type": "L+T", "credit": 2, "full_marks": 50},
        {"code": "ME 158", "name": "Engineering Drawing", "type": "P", "credit": 0, "full_marks": 50},
        {"code": "CE 151", "name": "Strength of Materials", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CE 151", "name": "Strength of Materials", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 152", "name": "Engineering Geology II", "type": "L+T", "credit": 2, "full_marks": 50},
        {"code": "CE 152", "name": "Engineering Geology II", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 153", "name": "Engineering Survey I", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CE 153", "name": "Engineering Survey I", "type": "P", "credit": 0, "full_marks": 50},
    ],
    "Year 2 - Part I": [
        {"code": "SH 201", "name": "Engineering Mathematics III", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "SH 202", "name": "Numerical Methods", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "SH 202", "name": "Numerical Methods", "type": "P", "credit": 0, "full_marks": 50},
        {"code": "CE 201", "name": "Fluid Mechanics", "type": "L+T", "credit": 4, "full_marks": 100},
        {"code": "CE 201", "name": "Fluid Mechanics", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 202", "name": "Theory of Structures I", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CE 202", "name": "Theory of Structures I", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 203", "name": "Engineering Survey II", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CE 203", "name": "Engineering Survey II", "type": "P", "credit": 0, "full_marks": 50},
        {"code": "CE 204", "name": "Computer Aided Civil Drawing", "type": "L+T", "credit": 2, "full_marks": 50},
        {"code": "CE 204", "name": "Computer Aided Civil Drawing", "type": "P", "credit": 0, "full_marks": 50},
        {"code": "CE 205", "name": "Concrete Technology", "type": "L+T", "credit": 2, "full_marks": 50},
        {"code": "CE 205", "name": "Concrete Technology", "type": "P", "credit": 0, "full_marks": 25},
    ],
    "Year 2 - Part II": [
        {"code": "SH 251", "name": "Communication English", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "SH 251", "name": "Communication English", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "SH 252", "name": "Probability and Statistics", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CE 251", "name": "Hydraulics", "type": "L+T", "credit": 4, "full_marks": 100},
        {"code": "CE 251", "name": "Hydraulics", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 252", "name": "Theory of Structures II", "type": "L+T", "credit": 4, "full_marks": 100},
        {"code": "CE 252", "name": "Theory of Structures II", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 253", "name": "Soil Mechanics", "type": "L+T", "credit": 4, "full_marks": 100},
        {"code": "CE 253", "name": "Soil Mechanics", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 254", "name": "Water Supply Engineering", "type": "L+T", "credit": 3, "full_marks": 100},
        {"code": "CE 254", "name": "Water Supply Engineering", "type": "P", "credit": 0, "full_marks": 25},
        {"code": "CE 255", "name": "Building Technology", "type": "L+T", "credit": 2, "full_marks": 50},
        {"code": "CE 256", "name": "Survey Camp", "type": "P", "credit": 2, "full_marks": 100},
    ]
}

# ==================== CORE CALCULATION LOGIC ====================

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

# ==================== SESSION STATE INITIALIZATION ====================

if 'semester_marks' not in st.session_state:
    st.session_state.semester_marks = {
        "Year 1 - Part I": {},
        "Year 1 - Part II": {},
        "Year 2 - Part I": {},
        "Year 2 - Part II": {}
    }

if 'current_semester' not in st.session_state:
    st.session_state.current_semester = "Year 1 - Part I"

# ==================== UI COMPONENTS ====================

def render_header():
    """Render application header"""
    st.title("🎓 GPA Calculator - Civil Engineering")
    st.markdown("**Bachelor in Civil Engineering (First 4 Semesters)**")
    
    with st.expander("ℹ️ **How to Use - Read First**", expanded=False):
        st.markdown("""
        ### How to Use This Calculator:
        1. **Select your semester** from the sidebar
        2. **Enter your marks** in the input boxes for each subject
        3. **Your GPA is calculated automatically** as you enter marks
        4. **Switch between semesters** to enter marks for different semesters
        5. **View Cumulative GPA** across all semesters at the bottom
        
        ### Important Notes:
        - ✅ All subjects and credits are **pre-filled** based on your curriculum
        - ✅ Theory (L+T) and Practical (P) are **separate** - enter marks for each
        - ✅ Leave blank if you haven't taken the exam yet
        - ✅ Marks are **automatically saved** as you type
        - ✅ Export your data using the sidebar options
        
        ### Grading Scale:
        """)
        
        # Display grade table
        grade_df = pd.DataFrame(GRADE_TABLE)
        grade_df = grade_df[['min', 'max', 'grade', 'point']]
        grade_df.columns = ['Min %', 'Max %', 'Grade', 'Grade Point']
        st.table(grade_df)

def render_semester_selector():
    """Render semester selection"""
    st.sidebar.title("📚 Semester Selection")
    
    semester_list = list(CIVIL_ENGINEERING_CURRICULUM.keys())
    
    st.sidebar.markdown(f"### Current: {st.session_state.current_semester}")
    st.sidebar.markdown("---")
    
    # Semester buttons
    for semester in semester_list:
        if st.sidebar.button(
            f"{'✅' if semester == st.session_state.current_semester else '📖'} {semester}",
            use_container_width=True,
            type="primary" if semester == st.session_state.current_semester else "secondary"
        ):
            st.session_state.current_semester = semester
            st.rerun()

def render_marks_input():
    """Render marks input interface for current semester"""
    current_sem = st.session_state.current_semester
    curriculum = CIVIL_ENGINEERING_CURRICULUM[current_sem]
    marks_data = st.session_state.semester_marks[current_sem]
    
    st.subheader(f"📝 Enter Marks - {current_sem}")
    st.markdown("*Enter marks obtained for each component. Leave blank if not taken yet.*")
    st.markdown("---")
    
    # Group by subject code
    subjects_by_code = {}
    for subject in curriculum:
        code = subject['code']
        if code not in subjects_by_code:
            subjects_by_code[code] = []
        subjects_by_code[code].append(subject)
    
    # Display each subject
    for code, components in subjects_by_code.items():
        # Subject header
        subject_name = components[0]['name']
        
        with st.container():
            st.markdown(f"### {subject_name}")
            st.markdown(f"**Course Code:** {code}")
            
            cols = st.columns([2, 1, 1, 2, 1, 1, 1])
            cols[0].markdown("**Component**")
            cols[1].markdown("**Credit**")
            cols[2].markdown("**Full Marks**")
            cols[3].markdown("**Enter Marks**")
            cols[4].markdown("**%**")
            cols[5].markdown("**Grade**")
            cols[6].markdown("**GP**")
            
            for component in components:
                key = f"{component['code']}_{component['type']}"
                cols = st.columns([2, 1, 1, 2, 1, 1, 1])
                
                # Component type
                cols[0].markdown(f"**{component['type']}**")
                
                # Credit (show only if > 0)
                if component['credit'] > 0:
                    cols[1].markdown(f"{component['credit']:.1f}")
                else:
                    cols[1].markdown("-")
                
                # Full marks
                cols[2].markdown(f"{component['full_marks']}")
                
                # Marks input
                current_marks = marks_data.get(key, None)
                marks_input = cols[3].number_input(
                    f"Marks for {key}",
                    min_value=0.0,
                    max_value=float(component['full_marks']),
                    value=float(current_marks) if current_marks is not None else 0.0,
                    step=0.5,
                    format="%.1f",
                    key=f"input_{key}",
                    label_visibility="collapsed"
                )
                
                # Update marks in session state
                if marks_input > 0:
                    st.session_state.semester_marks[current_sem][key] = marks_input
                
                    # Calculate and display grade info
                    percentage = calculate_percentage(marks_input, component['full_marks'])
                    grade, grade_point = assign_grade(percentage)
                    
                    cols[4].markdown(f"{percentage:.1f}")
                    cols[5].markdown(f"**{grade}**")
                    
                    if component['credit'] > 0:
                        cols[6].markdown(f"{grade_point:.1f}")
                    else:
                        cols[6].markdown("-")
                else:
                    cols[4].markdown("-")
                    cols[5].markdown("-")
                    cols[6].markdown("-")
            
            st.markdown("---")

def render_semester_results():
    """Render GPA results for current semester"""
    current_sem = st.session_state.current_semester
    marks_data = st.session_state.semester_marks[current_sem]
    
    # Check if any marks are entered
    if not any(marks_data.values()):
        st.info("📋 Enter marks above to see your GPA calculation")
        return
    
    st.markdown("---")
    st.subheader(f"📊 {current_sem} Results")
    
    # Calculate semester GPA
    sem_gpa, sem_weighted, sem_credits = calculate_semester_gpa(marks_data, current_sem)
    
    # Get total possible credits for the semester
    total_possible_credits = sum(s['credit'] for s in CIVIL_ENGINEERING_CURRICULUM[current_sem] if s['credit'] > 0)
    
    # Display results
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"Semester GPA",
            value=f"{sem_gpa:.2f}" if sem_credits > 0 else "0.00",
            help="Credit-weighted average of grade points"
        )
    
    with col2:
        st.metric(
            label="Credits Earned",
            value=f"{sem_credits:.1f}",
            help="Total credits from entered marks"
        )
    
    with col3:
        st.metric(
            label="Total Credits",
            value=f"{total_possible_credits:.1f}",
            help="Total credits available in this semester"
        )
    
    with col4:
        completion = (sem_credits / total_possible_credits * 100) if total_possible_credits > 0 else 0
        st.metric(
            label="Completion",
            value=f"{completion:.0f}%",
            help="Percentage of semester completed"
        )

def render_cumulative_gpa():
    """Render cumulative GPA across all semesters"""
    # Check if marks exist in any semester
    has_marks = any(
        any(marks.values()) 
        for marks in st.session_state.semester_marks.values()
    )
    
    if not has_marks:
        return
    
    st.markdown("---")
    st.markdown("---")
    st.subheader("🎯 Cumulative GPA (All Semesters)")
    
    # Calculate cumulative GPA
    cgpa, cgpa_weighted, cgpa_credits = calculate_cumulative_gpa(st.session_state.semester_marks)
    
    # Calculate total possible credits across all semesters
    total_possible_credits = sum(
        sum(s['credit'] for s in curriculum if s['credit'] > 0)
        for curriculum in CIVIL_ENGINEERING_CURRICULUM.values()
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Cumulative GPA",
            value=f"{cgpa:.2f}" if cgpa_credits > 0 else "0.00",
            help="Overall GPA across all semesters"
        )
    
    with col2:
        st.metric(
            label="Total Credits Earned",
            value=f"{cgpa_credits:.1f}",
            help="Sum of all credits from entered marks"
        )
    
    with col3:
        st.metric(
            label="Total Possible Credits",
            value=f"{total_possible_credits:.1f}",
            help="Total credits in first 4 semesters"
        )
    
    with col4:
        overall_completion = (cgpa_credits / total_possible_credits * 100) if total_possible_credits > 0 else 0
        st.metric(
            label="Overall Progress",
            value=f"{overall_completion:.0f}%",
            help="Percentage of total program completed"
        )
    
    # Display semester-wise breakdown
    st.markdown("### 📈 Semester-wise Breakdown")
    
    breakdown_data = []
    for sem_name in CIVIL_ENGINEERING_CURRICULUM.keys():
        marks_data = st.session_state.semester_marks[sem_name]
        if any(marks_data.values()):
            gpa, weighted, credits = calculate_semester_gpa(marks_data, sem_name)
            breakdown_data.append({
                "Semester": sem_name,
                "GPA": f"{gpa:.2f}",
                "Credits": f"{credits:.1f}",
                "Weighted Points": f"{weighted:.2f}"
            })
    
    if breakdown_data:
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)

def render_export_options():
    """Render data export options"""
    # Check if any marks are entered
    has_marks = any(
        any(marks.values()) 
        for marks in st.session_state.semester_marks.values()
    )
    
    if not has_marks:
        return
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 💾 Export Data")
    
    # Prepare export data
    export_data = []
    
    for sem_name, marks_data in st.session_state.semester_marks.items():
        curriculum = CIVIL_ENGINEERING_CURRICULUM[sem_name]
        
        for subject in curriculum:
            key = f"{subject['code']}_{subject['type']}"
            marks = marks_data.get(key, None)
            
            if marks is not None and marks > 0:
                percentage = calculate_percentage(marks, subject['full_marks'])
                grade, grade_point = assign_grade(percentage)
                
                export_data.append({
                    'Semester': sem_name,
                    'Course Code': subject['code'],
                    'Subject': subject['name'],
                    'Component': subject['type'],
                    'Credit': subject['credit'],
                    'Full Marks': subject['full_marks'],
                    'Marks Obtained': marks,
                    'Percentage': f"{percentage:.2f}",
                    'Grade': grade,
                    'Grade Point': grade_point,
                })
    
    if export_data:
        df_export = pd.DataFrame(export_data)
        
        # CSV download
        csv = df_export.to_csv(index=False)
        st.sidebar.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"civil_gpa_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # JSON download
        json_data = json.dumps(st.session_state.semester_marks, indent=2)
        st.sidebar.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name=f"civil_gpa_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True
        )

def render_clear_data():
    """Render clear all data option"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚠️ Reset Data")
    
    if st.sidebar.button("🗑️ Clear All Marks", use_container_width=True, type="secondary"):
        if st.sidebar.checkbox("I confirm I want to delete all data"):
            st.session_state.semester_marks = {
                "Year 1 - Part I": {},
                "Year 1 - Part II": {},
                "Year 2 - Part I": {},
                "Year 2 - Part II": {}
            }
            st.sidebar.success("✅ All marks cleared!")
            st.rerun()

# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point"""
    
    # Render header
    render_header()
    
    # Render sidebar
    render_semester_selector()
    render_export_options()
    render_clear_data()
    
    # Render main content
    render_marks_input()
    render_semester_results()
    render_cumulative_gpa()
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 12px;'>
        <p><strong>Civil Engineering - Bachelor Program</strong></p>
        <p>Theory (L+T) and Practical (P) are graded separately | Credits used for weighting | Grades assigned based on percentage</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
