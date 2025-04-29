import streamlit as st
from candidate.candidate import candidate_page  # Corrected import path
from admin.admin import admin_page  # Corrected import path

# Set up page configuration
st.set_page_config(page_title="Candidate Evaluation App", layout="wide")

# App title
st.title("🏆 Candidate Evaluation App")

# Main page options for navigation
page = st.sidebar.radio("Choose a page", ("Home", "Candidate Page", "Admin Page"))

# Render appropriate page based on user selection
if page == "Home":
    st.write("""
    Welcome to the Candidate Evaluation Application.

    - Go to **Candidate Page** to manually enter responses.
    - Go to **Admin Page** to upload CSVs, evaluate all candidates, and select Top 3.
    """)

    # Button to clear all records from session state
    if st.button("Clear All Records"):
        st.session_state.clear()  # Clear all session state data
        st.success("✅ All records cleared!")

elif page == "Candidate Page":
    candidate_page()  # Render the candidate page

elif page == "Admin Page":
    admin_page()  # Render the admin page
