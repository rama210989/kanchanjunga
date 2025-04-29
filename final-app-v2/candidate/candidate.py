import streamlit as st

def candidate_page():
    st.title("✍️ Candidate Submission")

    if "candidates" not in st.session_state:
        st.session_state.candidates = []

    st.header("Enter Candidate Details")

    with st.form("candidate_form"):
        name = st.text_input("Candidate Name", key="name")
        response_1 = st.text_area("Q1: Tell us about yourself")
        response_2 = st.text_area("Q2: Why do you want this role?")
        response_3 = st.text_area("Q3: Describe a challenge you faced.")
        response_4 = st.text_area("Q4: How do you handle feedback?")
        response_5 = st.text_area("Q5: Where do you see yourself in 5 years?")
        
        submitted = st.form_submit_button("Submit")

        if submitted:
            if name.strip() == "":
                st.error("Candidate name is mandatory!")
            else:
                st.session_state.candidates.append({
                    "name": name,
                    "responses": [response_1, response_2, response_3, response_4, response_5]
                })
                st.success(f"Responses submitted for {name} ✅")
