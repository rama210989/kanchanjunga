import streamlit as st
import pandas as pd
import openai

def admin_page():
    # Set up page title
    st.title("🛠️ Admin Panel")

    # Set OpenAI API key
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    # Initialize session states
    if "candidates" not in st.session_state:
        st.session_state.candidates = []

    if "evaluated_candidates" not in st.session_state:
        st.session_state.evaluated_candidates = []

    # Upload CSV file
    st.header("Upload Candidate Responses (Optional)")
    uploaded_file = st.file_uploader("Upload CSV file with 6 columns (Name, Q1, Q2, Q3, Q4, Q5)", type=["csv"])

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
                st.success(f"Uploaded {len(df)} candidates!")
        except Exception as e:
            st.error(f"Error reading the CSV file: {e}")

    st.divider()

    # Evaluate candidates
    if st.button("🚀 Evaluate All Candidates"):
        evaluated = []
        for candidate in st.session_state.candidates:
            evaluations = []
            scores = []
            response_evaluations = []  # To hold the evaluation response text for each question

            for response in candidate["responses"]:
                prompt = f"Evaluate the following response on a scale of 1-10:\n\n'{response}'\n\nScore (only number):"
                try:
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    evaluation_text = completion.choices[0].message.content.strip()

                    try:
                        score = int(evaluation_text)
                    except:
                        score = 5  # Default fallback score
                    
                    evaluations.append(evaluation_text)  # Add the evaluation response
                    scores.append(score)  # Add the score
                    response_evaluations.append((evaluation_text, score))  # Tuple of response evaluation and score

                except Exception as e:
                    st.error(f"OpenAI Error: {e}")
                    evaluations.append("N/A")
                    scores.append(5)
                    response_evaluations.append(("Error in evaluation", 5))  # Handle error response gracefully

            total_score = sum(scores)
            percentage = round((total_score / 50) * 100, 2)

            evaluated.append({
                "Name": candidate["name"],
                "Responses": candidate["responses"],
                "Evaluations": evaluations,
                "Scores": scores,
                "Response Evaluations": response_evaluations,  # Store responses with evaluations
                "Total Score": total_score,
                "Percentage": percentage
            })

        st.session_state.evaluated_candidates = evaluated
        st.success("✅ Evaluation Complete!")

    # Display evaluation results
    st.divider()

    if st.session_state.evaluated_candidates:
        st.subheader("📊 Full Evaluation Results")

        for candidate in st.session_state.evaluated_candidates:
            st.markdown(f"### {candidate['Name']}")
            for idx in range(5):
                st.write(f"**Q{idx+1}:** {candidate['Responses'][idx]}")
                st.write(f"**Evaluation:** {candidate['Evaluations'][idx]}")
                st.write(f"**Score:** {candidate['Scores'][idx]}/10")
                st.write(f"**Evaluation Response:** {candidate['Response Evaluations'][idx][0]}")  # Display evaluation text
                st.write(f"**Score for Evaluation:** {candidate['Response Evaluations'][idx][1]}/10")  # Display score for evaluation
                st.write("---")
            st.write(f"**Total Score:** {candidate['Total Score']}/50")
            st.write(f"**Percentage:** {candidate['Percentage']}%")
            st.divider()

        if st.button("🏆 Shortlist Top 3 Candidates"):
            top3 = sorted(st.session_state.evaluated_candidates, key=lambda x: x["Percentage"], reverse=True)[:3]
            st.subheader("🥇 Top 3 Candidates:")
            for idx, candidate in enumerate(top3, start=1):
                st.write(f"{idx}. **{candidate['Name']}** - {candidate['Percentage']}%")
