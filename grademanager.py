import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Student Grade Manager",
    page_icon="🎓",
    layout="wide",
)

# Custom CSS for Google Material Design Typography & Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
    }
    .main .block-container {
        max-width: 900px;
        padding-top: 2rem;
    }
    div.stButton > button[kind="primary"] {
        background-color: #1a73e8 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def get_grade(mark: float) -> str:
    """Return letter grade based on mark."""
    if mark >= 90:
        return "A+"
    elif mark >= 80:
        return "A"
    elif mark >= 70:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 50:
        return "D"
    else:
        return "F"


# Initialize Session State
if "students" not in st.session_state:
    st.session_state.students = []

# Title & Subtitle
st.title("🎓 Student Grade Manager")
st.caption("Manage student marks and track real-time class metrics.")

# Input Card Container
with st.container(border=True):
    st.subheader("Add Student")
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input("Full Name", placeholder="e.g., Karthick")
        with col2:
            mark = st.number_input(
                "Mark (0 - 100)",
                min_value=0.0,
                max_value=100.0,
                value=75.0,
                step=1.0,
            )

        submitted = st.form_submit_button("Add Student", type="primary")
        if submitted:
            clean_name = name.strip()
            if not clean_name:
                st.error("Please enter a valid student name.")
            else:
                grade = get_grade(mark)
                st.session_state.students.append(
                    {
                        "Name": clean_name,
                        "Mark": float(mark),
                        "Grade": grade,
                    }
                )
                st.success(f"Added **{clean_name}** ({mark:.0f} - {grade})")

# Results and Metrics Section
if st.session_state.students:
    st.markdown("---")

    # Metrics Summary
    marks = [s["Mark"] for s in st.session_state.students]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Students", len(marks))
    m2.metric("Class Average", f"{sum(marks)/len(marks):.1f}")
    m3.metric("Highest Mark", f"{max(marks):.1f}")
    m4.metric("Lowest Mark", f"{min(marks):.1f}")

    st.markdown("### 📋 Student Roster")

    # Create DataFrame
    df = pd.DataFrame(st.session_state.students)

    # Render Clean Native Streamlit Dataframe
    st.dataframe(
        df,
        column_config={
            "Name": st.column_config.TextColumn("Student Name"),
            "Mark": st.column_config.NumberColumn(
                "Mark", format="%.1f"
            ),
            "Grade": st.column_config.TextColumn("Grade"),
        },
        use_container_width=True,
        hide_index=True,
    )

    # Action Bar
    if st.button("Clear Roster"):
        st.session_state.students = []
        st.rerun()

else:
    st.markdown("---")
    st.info("No students added yet. Use the form above to add your first student.")