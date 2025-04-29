import streamlit as st
import openai

def candidate_page():
    st.header("🧑‍💼 Candidate Interview Form")

    # Define the questions
    questions = [
        "What's your name?",
        "What do you know about our company?",
        "Why do you want to join our company?",
        "What are your biggest strengths?",
        "What are your salary expectations?"
    ]

    # Store answers
    answers = []

    # Create input form
    with st.form("candidate_form"):
        candidate_name = st.text_input("Candidate Name")
        for i, q in enumerate(questions):
            answers.append(st.text_area(f"Q{i+1}: {q}", key=f"q{i}"))

        submitted = st.form_submit_button("Submit Responses")

    # Refresh button
    if st.button("🔄 Refresh"):
        st.experimental_rerun()

    if submitted:
        # GPT evaluation
        gpt_feedbacks = []
        gpt_scores = []

        for q, a in zip(questions, answers):
            prompt = f"""
Question: {q}
Candidate's Answer: {a}

Evaluate the answer in 1-2 lines. Then give a score out of 10.
"""
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                content = response["choices"][0]["message"]["content"]
                gpt_feedbacks.append(content)

                # Extract score
                lines = content.splitlines()
                score_line = next((line for line in lines if "Score" in line), "Score: 0/10")
                score = int(score_line.split(":")[1].split("/")[0].strip())
                gpt_scores.append(score)

            except Exception as e:
                gpt_feedbacks.append(f"Error during evaluation: {str(e)}")
                gpt_scores.append(0)

        total_score = sum(gpt_scores)

        # Save to session state
        if "all_candidates" not in st.session_state:
            st.session_state["all_candidates"] = []

        # Append candidate responses and evaluations to session state
        st.session_state["all_candidates"].append({
            "name": candidate_name,
            "questions": questions,
            "answers": answers,
            "feedbacks": gpt_feedbacks,
            "scores": gpt_scores,
            "total_score": total_score
        })

        st.success(f"✅ Responses submitted and evaluated for {candidate_name}!")

        # Display submission confirmation with summary
        st.write(f"### Summary for {candidate_name}:")
        for i, (q, a, feedback, score) in enumerate(zip(questions, answers, gpt_feedbacks, gpt_scores)):
            st.write(f"**Q{i+1}: {q}**")
            st.write(f"Answer: {a}")
            st.write(f"Evaluation: {feedback}")
            st.write(f"Score: {score}/10")
        
        st.write(f"**Total Score: {total_score}/50**")
