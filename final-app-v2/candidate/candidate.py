import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def candidate_page():
    st.title("🤖 Candidate Chatbot")

    # Initialize session state for candidate responses
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = ""
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
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

    # Display questions and collect responses
    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        answer = st.text_area(f"Q{st.session_state.current_question + 1}: {question}")
        if st.button("Next"):
            if answer.strip() != "":
                st.session_state.responses.append(answer)
                st.session_state.current_question += 1
                st.experimental_rerun()
            else:
                st.warning("Please enter your response before continuing.")
    elif st.session_state.current_question == len(questions):
        st.success("🎉 Thank you for completing the questions!")
        if st.button("Submit Responses"):
            # After submission, trigger the evaluation process
            st.session_state.evaluated = False
            st.experimental_rerun()

    if st.button("Refresh"):
        # Reset everything for the next candidate
        st.session_state.candidate_name = ""
        st.session_state.current_question = 0
        st.session_state.responses = []
        st.session_state.evaluated = False
        st.experimental_rerun()
