import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def candidate_page():
    st.title("📝 Candidate Evaluation Form")

    questions = [
        "Tell us about yourself.",
        "Why do you want this role?",
        "Describe a challenge you faced.",
        "How do you handle feedback?",
        "Where do you see yourself in 5 years?"
    ]

    with st.form("candidate_form"):
        candidate_name = st.text_input("Your Name")

        answers = []
        for i, question in enumerate(questions):
            answer = st.text_area(f"Q{i+1}: {question}", key=f"q_{i}")
            answers.append(answer)

        submitted = st.form_submit_button("Submit")

    if submitted:
        if not candidate_name.strip() or any(ans.strip() == "" for ans in answers):
            st.warning("Please fill out all questions and your name before submitting.")
            return

        with st.spinner("Evaluating your responses..."):
            evaluations = []
            scores = []

            for r in answers:
                prompt = f"Evaluate the following response on a scale of 1-10, with detailed feedback:\n\n'{r}'"
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = completion.choices[0].message.content.strip()
                    score = int(''.join(filter(str.isdigit, result.split()[0]))) if result else 5
                except Exception as e:
                    result = "Error in evaluation"
                    score = 5
                evaluations.append(result)
                scores.append(score)

            total_score = sum(scores)
            percentage = round((total_score / 50) * 100, 2)

            st.success("🎉 Evaluation Complete!")
            st.header(f"📋 Feedback for {candidate_name}")
            for i in range(5):
                st.markdown(f"**Q{i+1}:** {questions[i]}")
                st.markdown(f"**Your Answer:** {answers[i]}")
                st.markdown(f"**Evaluation:** {evaluations[i]}")
                st.markdown(f"**Score:** {scores[i]}/10")
                st.markdown("---")
            st.subheader(f"✅ Total Score: {total_score}/50 ({percentage}%)")

            # Optionally store feedback in session
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
