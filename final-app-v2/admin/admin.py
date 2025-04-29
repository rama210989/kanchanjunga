import streamlit as st
import pandas as pd
import openai

def admin_page():
    st.title("🛠️ Admin Panel")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    if "candidates" not in st.session_state:
        st.session_state.candidates = []

    if "evaluated_candidates" not in st.session_state:
        st.session_state.evaluated_candidates = []

    # --- 📝 Manual Candidate Entry ---
    st.header("Manually Add a Candidate")
    with st.form("manual_candidate_form"):
        name = st.text_input("Candidate Name")
        q1 = st.text_area("Q1 Response")
        q2 = st.text_area("Q2 Response")
        q3 = st.text_area("Q3 Response")
        q4 = st.text_area("Q4 Response")
        q5 = st.text_area("Q5 Response")
        submitted = st.form_submit_button("➕ Add Candidate")

        if submitted:
            if all([name, q1, q2, q3, q4, q5]):
                st.session_state.candidates.append({
                    "name": name,
                    "responses": [q1, q2, q3, q4, q5]
                })
                st.success(f"✅ Candidate '{name}' added successfully.")
            else:
                st.error("⚠️ Please fill in all fields.")

    st.divider()

    # --- 📤 Upload CSV ---
    st.header("Upload Candidate Responses (Optional)")
    uploaded_file = st.file_uploader("Upload CSV with 6 columns: Name, Q1, Q2, Q3, Q4, Q5", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = ["Name", "Q1", "Q2", "Q3", "Q4", "Q5"]
            if not all(col in df.columns for col in required_columns):
                st.error("CSV must have columns: Name, Q1, Q2, Q3, Q4, Q5")
            else:
                for _, row in df.iterrows():
                    st.session_state.candidates.append({
                        "name": row["Name"],
                        "responses": [row["Q1"], row["Q2"], row["Q3"], row["Q4"], row["Q5"]]
                    })
                st.success(f"Uploaded {len(df)} candidates from CSV!")
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")

    st.divider()

    # --- 🚀 Evaluate All Candidates ---
    if st.button("🚀 Evaluate All Candidates"):
        evaluated = []
        for candidate in st.session_state.candidates:
            evaluations = []
            scores = []

            for response in candidate["responses"]:
                prompt = f"Evaluate the following response on a scale of 1-10, providing detailed reasoning:\n\n'{response}'\n\nScore (only number):"
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    evaluation_text = completion.choices[0].message.content.strip()
                    try:
                        score = int(''.join(filter(str.isdigit, evaluation_text.split()[0])))  # safer parsing
                    except:
                        score = 5
                    evaluations.append(evaluation_text)
                    scores.append(score)
                except Exception as e:
                    st.error(f"OpenAI Error: {e}")
                    evaluations.append("Error in evaluation")
                    scores.append(5)

            total_score = sum(scores)
            percentage = round((total_score / 50) * 100, 2)

            evaluated.append({
                "Name": candidate["name"],
                "Responses": candidate["responses"],
                "Evaluations": evaluations,
                "Scores": scores,
                "Total Score": total_score,
                "Percentage": percentage
            })

        st.session_state.evaluated_candidates = evaluated
        st.success("✅ Evaluation Complete!")

    # --- 📊 Show Results ---
    st.divider()
    if st.session_state.evaluated_candidates:
        st.subheader("📊 Full Evaluation Results")

        for candidate in st.session_state.evaluated_candidates:
            st.markdown(f"### {candidate['Name']}")
            for idx in range(5):
                st.write(f"**Q{idx+1}:** {candidate['Responses'][idx]}")
                st.write(f"**Evaluation:** {candidate['Evaluations'][idx]}")
                st.write(f"**Score:** {candidate['Scores'][idx]}/10")
                st.write("---")
            st.write(f"**Total Score:** {candidate['Total Score']}/50")
            st.write(f"**Percentage:** {candidate['Percentage']}%")
            st.divider()

        # --- 🏆 Shortlist Top 3 ---
        if st.button("🏆 Shortlist Top 3 Candidates"):
            top3 = sorted(st.session_state.evaluated_candidates, key=lambda x: x["Percentage"], reverse=True)[:3]
            st.subheader("🥇 Top 3 Candidates:")
            for idx, candidate in enumerate(top3, start=1):
                st.write(f"{idx}. **{candidate['Name']}** - {candidate['Percentage']}%")
