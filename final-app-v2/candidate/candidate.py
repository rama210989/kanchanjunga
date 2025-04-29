import streamlit as st
import openai
import re

openai.api_key = st.secrets["OPENAI_API_KEY"]

def candidate_page():
    st.title("📝 Candidate Evaluation Form")

    questions = [
        "What do you know about our company?",
        "Why do you want to join our company?",
        "What are your biggest strengths?",
        "What are your salary expectations?"
    ]

    with st.form("candidate_form"):
        candidate_name = st.text_input("What's your name?")
        answers = []
        for i, question in enumerate(questions):
            answer = st.text_area(f"Q{i+1}: {question}", key=f"q_{i}")
            answers.append(answer)
        submitted = st.form_submit_button("Submit")

    if submitted:
        if not candidate_name.strip() or any(ans.strip() == "" for ans in answers):
            st.warning("Please fill out all fields before submitting.")
            return

        with st.spinner("Evaluating your responses..."):
            evaluations = []
            scores = []

            for r in answers:
                prompt = f"Evaluate the following candidate response on a scale of 1-10. Start with the score (e.g. '7/10'), followed by brief constructive feedback:\n\nResponse: '{r}'"
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = completion.choices[0].message.content.strip()
                    
                    # Extract score using regex
                    match = re.search(r"\b(\d{1,2})\s*/\s*10\b", result)
                    score = int(match.group(1)) if match else 5

                except Exception as e:
                    result = "Error in evaluation"
                    score = 5

                evaluations.append(result)
                scores.append(score)

            total_score = sum(scores)
            percentage = round((total_score / 40) * 100, 2)  # 4 questions x 10

            st.success("🎉 Evaluation Complete!")
            st.header(f"📋 Feedback for {candidate_name}")
            for i in range(len(questions)):
                st.markdown(f"**Q{i+1}:** {questions[i]}")
                st.markdown(f"**Your Answer:** {answers[i]}")
                st.markdown(f"**Evaluation:** {evaluations[i]}")
                st.markdown(f"**Score:** {scores[i]}/10")
                st.markdown("---")
            st.subheader(f"✅ Total Score: {total_score}/40 ({percentage}%)")

            # Optionally store feedback
            if "manual_candidates" not in st.session_state:
                st.session_state.manual_candidates = []
            st.session_state.manual_candidates.append({
                "name": candidate_name,
                "responses": answers,
                "evaluations": evaluations,
                "scores": scores,
                "total": total_score,
                "percent": percentage
            })
