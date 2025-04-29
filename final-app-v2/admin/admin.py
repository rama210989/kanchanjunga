import streamlit as st
import pandas as pd
import openai

def admin_page():
    st.title("🛠️ Admin Panel")
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    if "manual_candidates" not in st.session_state:
        st.session_state.manual_candidates = []
    if "csv_candidates" not in st.session_state:
        st.session_state.csv_candidates = []
    if "evaluated_all" not in st.session_state:
        st.session_state.evaluated_all = []

    st.header("📤 Upload Candidate Responses (CSV)")
    uploaded_file = st.file_uploader("Upload CSV with columns: Name, Q1, Q2, Q3, Q4, Q5", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if not all(col in df.columns for col in ["Name", "Q1", "Q2", "Q3", "Q4", "Q5"]):
            st.error("❌ CSV must contain: Name, Q1, Q2, Q3, Q4, Q5")
        else:
            st.session_state.csv_candidates = []
            for _, row in df.iterrows():
                st.session_state.csv_candidates.append({
                    "name": row["Name"],
                    "responses": [row["Q1"], row["Q2"], row["Q3"], row["Q4"], row["Q5"]]
                })
            st.success(f"✅ Uploaded {len(df)} candidates.")

    st.divider()

    if st.button("🚀 Evaluate All Candidates"):
        combined = st.session_state.manual_candidates + st.session_state.csv_candidates
        evaluated = []

        for c in combined:
            evaluations = []
            scores = []
            for r in c["responses"]:
                prompt = f"Evaluate the following response on a scale of 1-10 with detailed feedback:\n\n'{r}'"
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    result = completion.choices[0].message.content.strip()
                    score = int(''.join(filter(str.isdigit, result.split()[0]))) if result else 5
                except:
                    result = "Error in evaluation"
                    score = 5
                evaluations.append(result)
                scores.append(score)

            total_score = sum(scores)
            percent = round((total_score / 50) * 100, 2)

            evaluated.append({
                "name": c["name"],
                "responses": c["responses"],
                "evaluations": evaluations,
                "scores": scores,
                "total": total_score,
                "percent": percent
            })

        st.session_state.evaluated_all = evaluated
        st.success("✅ All candidates evaluated!")

    st.divider()
    if st.session_state.evaluated_all:
        st.subheader("📊 Evaluation Results")
        for c in st.session_state.evaluated_all:
            st.markdown(f"### {c['name']}")
            for i in range(5):
                st.markdown(f"**Q{i+1}:** {c['responses'][i]}")
                st.markdown(f"**Evaluation:** {c['evaluations'][i]}")
                st.markdown(f"**Score:** {c['scores'][i]}/10")
                st.markdown("---")
            st.write(f"**Total Score:** {c['total']}/50")
            st.write(f"**Percentage:** {c['percent']}%")
            st.divider()

        if st.button("🏆 Show Top 3"):
            top3 = sorted(st.session_state.evaluated_all, key=lambda x: x["percent"], reverse=True)[:3]
            st.subheader("🥇 Top 3 Candidates")
            for i, c in enumerate(top3, start=1):
                st.write(f"{i}. {c['name']} - {c['percent']}%")

