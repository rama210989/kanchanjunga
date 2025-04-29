import streamlit as st
import pandas as pd
import openai

def admin_page():
    st.header("📋 Summary Table")

    if "all_candidates" not in st.session_state or len(st.session_state["all_candidates"]) == 0:
        st.info("No candidates submitted yet.")
        return

    # Summary Table
    summary_data = [{
        "Candidate": c["name"],
        "Total Score": c["total_score"]
    } for c in st.session_state["all_candidates"]]
    st.dataframe(pd.DataFrame(summary_data))

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
        st.markdown(f"✅ **Total Score: {candidate['total_score']}/50**")

    # Upload CSV for bulk addition
    st.markdown("### 📥 Bulk Upload CSV for Candidates")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file is not None:
        # Read the CSV into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Ensure that the CSV has the necessary columns
        if set(['name', 'questions', 'answers']) <= set(df.columns):
            st.write("Preview of uploaded data:")
            st.dataframe(df)

            # Button to evaluate CSV entries
            if st.button("Evaluate and Append Entries"):
                for _, row in df.iterrows():
                    candidate_name = row['name']
                    answers = row['answers'].split(';')  # Assuming answers are semicolon-separated
                    gpt_feedbacks = []
                    gpt_scores = []

                    # Evaluate each answer using GPT
                    for q, a in zip(row['questions'].split(';'), answers):
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

                    # Append evaluated candidate to session state
                    st.session_state["all_candidates"].append({
                        "name": candidate_name,
                        "questions": row['questions'].split(';'),
                        "answers": answers,
                        "feedbacks": gpt_feedbacks,
                        "scores": gpt_scores,
                        "total_score": total_score
                    })

                st.success("✅ Evaluated and appended CSV entries successfully!")

        else:
            st.error("CSV file is missing required columns ('name', 'questions', 'answers').")
