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

elif page == "Candidate Page":
    candidate_page()  # Render the candidate page

elif page == "Admin Page":
    admin_page()  # Render the admin page
