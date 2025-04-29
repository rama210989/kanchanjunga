import streamlit as st
import pandas as pd
import openai

# Define questions (1st one is not evaluated)
questions = [
    "What's your name?",
    "What do you know about our company?",
    "Why do you want to join our company?",
    "What are your biggest strengths?",
    "What are your salary expectations?"
]

def evaluate_candidate(name, answers):
    gpt_feedbacks = []
    gpt_scores = []

    for q, a in zip(questions[1:], answers[1:]):  # Evaluate Q2–Q5
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
            gpt_feedbacks.append(f"Error: {str(e)}")
            gpt_scores.append(0)

    return {
        "name": name,
        "questions": questions[1:],      # Only evaluated ones
        "answers": answers[1:],          # Only evaluated answers
        "feedbacks": gpt_feedbacks,
        "scores": gpt_scores,
        "total_score": sum(gpt_scores)   # Out of 40
    }

def admin_page():
    st.header("📋 Summary Table")

    if "all_candidates" not in st.session_state:
        st.session_state["all_candidates"] = []

    if len(st.session_state["all_candidates"]) == 0:
        st.info("No candidates submitted yet.")
    else:
        # Summary Table
        summary_data = [{
            "Candidate": c["name"],
            "Total Score (out of 40)": c["total_score"]
        } for c in st.session_state["all_candidates"]]
        st.dataframe(pd.DataFrame(summary_data))

        # Detailed Evaluations
        st.markdown("### 📝 Detailed Evaluations")
        for idx, candidate in enumerate(st.session_state["all_candidates"], start=1):
            st.markdown(f"**{idx}. {candidate['name']}**")
            for i in range(len(candidate["questions"])):
                st.markdown(f"""
**Q{i+1}: {candidate['questions'][i]}**

**Answer:** {candidate['answers'][i]}

**Evaluation:** {candidate['feedbacks'][i]}

**Score:** {candidate['scores'][i]}/10
""")
            st.markdown(f"✅ **Total Score: {candidate['total_score']}/40**")

    # Bulk Upload
    st.markdown("### 📤 Upload Bulk Candidate Responses")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        required_cols = ["name", "answer_1", "answer_2", "answer_3", "answer_4", "answer_5"]

        if all(col in df.columns for col in required_cols):
            with st.spinner("Evaluating candidates..."):
                for _, row in df.iterrows():
                    answers = [row[f"answer_{i}"] for i in range(1, 6)]
                    entry = evaluate_candidate(row["name"], answers)
                    st.session_state["all_candidates"].append(entry)
            st.success("✅ Bulk candidates evaluated and added!")
        else:
            st.error(f"❌ CSV must have columns: {', '.join(required_cols)}")

    # Clear All Data
    st.markdown("### 🔄 Reset App")
    if st.button("Clear All Data"):
        st.session_state["all_candidates"] = []
        st.success("All candidate data cleared.")
        st.experimental_rerun()
