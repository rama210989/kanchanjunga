import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def candidate_page():
    st.title("🤖 Candidate Chatbot")
    
    if "candidate_name" not in st.session_state:
        st.session_state.candidate_name = ""
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "responses" not in st.session_state:
        st.session_state.responses = []
    if "evaluated" not in st.session_state:
        st.session_state.evaluated = False
    if "feedback" not in st.session_state:
        st.session_state.feedback = {}

    questions = [
        "Tell us about yourself.",
        "Why do you want this role?",
        "Describe a challenge you faced.",
        "How do you handle feedback?",
        "Where do you see yourself in 5 years?"
    ]

    if st.session_state.candidate_name == "":
        st.session_state.candidate_name = st.text_input("What's your name?")
        st.stop()

    if st.session_state.current_question < len(questions):
        question = questions[st.session_state.current_question]
        answer = st.text_area(f"Q{st.session_state.current_question+1}: {question}")
        if st.button("Next"):
            if answer.strip() != "":
                st.session_state.responses.append(answer)
                st.session_state.current_question += 1
                st.experimental_rerun()  # fallback that works in most stable versions
            else:
                st.warning("Please enter your response before continuing.")
    elif not st.session_state.evaluated:
        st.success("🎉 Thank you for completing all questions!")

        with st.spinner("Evaluating your responses..."):
            evaluations = []
            scores = []
            for r in st.session_state.responses:
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
            st.session_state.feedback = {
                "name": st.session_state.candidate_name,
                "responses": st.session_state.responses,
                "evaluations": evaluations,
                "scores": scores,
                "total": total_score,
                "percent": percentage
            }
            st.session_state.evaluated = True

    if st.session_state.evaluated:
        fb = st.session_state.feedback
        st.header(f"📋 Evaluation for {fb['name']}")
        for i in range(5):
            st.markdown(f"**Q{i+1}:** {questions[i]}")
            st.markdown(f"**Your Answer:** {fb['responses'][i]}")
            st.markdown(f"**Evaluation:** {fb['evaluations'][i]}")
            st.markdown(f"**Score:** {fb['scores'][i]}/10")
            st.markdown("---")
        st.subheader(f"✅ Total Score: {fb['total']}/50 ({fb['percent']}%)")

        if "manual_candidates" not in st.session_state:
            st.session_state.manual_candidates = []
        st.session_state.manual_candidates.append(fb)
