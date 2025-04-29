import streamlit as st

def candidate_page():
    st.title("🤖 Candidate Form")

    # Initialize session state for candidate responses
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = ""
    if "responses" not in st.session_state:
        st.session_state.responses = []

    questions = [
        "What's your name?",
        "What do you know about our company?", 
        "Why do you want to join our company?", 
        "What are your biggest strengths?", 
        "What are your salary expectations?"
    ]

    # Candidate name input
    if st.session_state.candidate_name == "":
        st.session_state.candidate_name = st.text_input("Enter your name:")
        st.stop()

    # Create a form for collecting responses
    with st.form(key="candidate_form"):
        responses = []
        for i, question in enumerate(questions):
            response = st.text_area(f"Q{i+1}: {question}")
            responses.append(response)

        submit_button = st.form_submit_button(label="Submit Responses")

    # Handle form submission
    if submit_button:
        if all(response.strip() != "" for response in responses):
            st.session_state.responses = responses
            st.session_state.evaluated = False
            st.success("🎉 Thank you for completing the questions!")
            st.experimental_rerun()
        else:
            st.warning("Please fill out all responses before submitting.")

    # Reset page for new candidate (refresh)
    if st.button("Refresh"):
        st.session_state.candidate_name = ""
        st.session_state.responses = []
        st.session_state.evaluated = False
        st.experimental_rerun()
