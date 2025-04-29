import streamlit as st

# Dummy evaluator function (replace with real logic)
def evaluate_candidate(responses):
    feedback = []
    total_score = 0
    for i, answer in enumerate(responses):
        score = min(len(answer.strip()) // 10, 10)  # Simple logic
        fb = f"Answer {i+1} evaluation: {score}/10"
        feedback.append(fb)
        total_score += score
    return total_score, feedback

def candidate_page():
    st.title("🤖 Candidate Interview Form")

    # Session storage for all candidates
    if "all_candidates" not in st.session_state:
        st.session_state["all_candidates"] = []

    with st.form("candidate_form"):
        name = st.text_input("Candidate Name")
        q1 = st.text_area("1. What do you know about our company?")
        q2 = st.text_area("2. Why do you want to join our company?")
        q3 = st.text_area("3. What are your biggest strengths?")
        q4 = st.text_area("4. What are your salary expectations?")
        q5 = st.text_area("5. Where do you see yourself in 5 years?")
        submit = st.form_submit_button("Submit")

    if submit:
        if all([name.strip(), q1, q2, q3, q4, q5]):
            answers = [q1, q2, q3, q4, q5]
            score, feedback = evaluate_candidate(answers)
            candidate_data = {
                "name": name,
                "answers": answers,
                "score": score,
                "feedback": feedback
            }
            st.session_state.all_candidates.append(candidate_data)
            st.success(f"Responses submitted for {name}!")

        else:
            st.error("Please answer all questions before submitting.")

    if st.button("Refresh"):
        st.experimental_rerun()
