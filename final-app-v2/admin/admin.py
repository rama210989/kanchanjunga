import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def admin_page():
    st.title("📊 Admin Section")

    # Initialize session state for admin evaluation results
    if "admin_results" not in st.session_state:
        st.session_state.admin_results = []

    if "evaluated" in st.session_state and st.session_state.evaluated:
        candidate_name = st.session_state.candidate_name
        responses = st.session_state.responses

        # Display a summary before evaluation
        st.subheader("Candidate Summary")
        st.write(f"**Candidate Name:** {candidate_name}")
        st.write(f"**Total Score:** {sum([score for score in st.session_state.scores])}/50")

        # Trigger evaluation
        st.spinner("Evaluating candidate's responses...")
        evaluations = []
        scores = []
        for r in responses:
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

        # Append the evaluation results to the admin section
        st.session_state.admin_results.append({
            "candidate_name": candidate_name,
            "responses": responses,
            "evaluations": evaluations,
            "scores": scores,
            "total_score": total_score,
            "percentage": percentage
        })

    # Display the evaluations in the admin section
    st.header("📋 Evaluations")
    if st.session_state.admin_results:
        for result in st.session_state.admin_results:
            st.markdown(f"**Candidate:** {result['candidate_name']}")
            for i, eval_result in enumerate(result['evaluations']):
                st.markdown(f"**Q{i+1}:** {eval_result}")
                st.markdown(f"**Score:** {result['scores'][i]}/10")
            st.markdown(f"**Total Score:** {result['total_score']}/50 ({result['percentage']}%)")
            st.markdown("---")
