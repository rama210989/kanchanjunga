import openai
import pandas as pd
import streamlit as st
import re
import random

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# List of 5 predefined questions
questions_list = [
    "Why do you want to work with us?",
    "What is your greatest strength?",
    "What do you know about our company?",
    "Where do you see yourself in 5 years?",
    "What are your salary expectations?"
]

# Function to evaluate the answer
def evaluate_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\n\nEvaluate this response on a scale of 1 to 10 and explain why."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI that evaluates interview answers on a scale of 1 to 10."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        evaluation = response['choices'][0]['message']['content'].strip()

        # Use regular expression to extract a score between 1 and 10
        score_match = re.search(r'(\d+)', evaluation)
        if score_match:
            return int(score_match.group(1)), evaluation
        else:
            return None, evaluation
    except Exception as e:
        return None, f"Error evaluating answer: {e}"

# Streamlit UI Components
st.title("Interview Question Evaluator")

# Define pages
PAGES = {
    "Candidate": "candidate_page",
    "Admin": "admin_page"
}

# Sidebar navigation
page = st.sidebar.radio("Select your role", options=PAGES.keys())

# Candidate Page
if page == "Candidate":
    st.subheader("Candidate Page")
    
    # Initialize session state if it doesn't exist
    if "candidates" not in st.session_state:
        st.session_state.candidates = []

    # Candidate Name Input
    name = st.text_input("Enter your name")

    # Dictionary to store answers
    answers = {}
    for question in questions_list:
        answers[question] = st.text_area(question)

    # Submit Answers Button
    if st.button("Submit Answers"):
        if not name.strip():
            st.error("Name is mandatory. Please enter your name.")
        elif any(not ans.strip() for ans in answers.values()):
            st.error("Please answer all questions before submitting.")
        else:
            evaluations = []
            total_score = 0
            for question, answer in answers.items():
                score, evaluation = evaluate_answer(question, answer)
                evaluations.append({
                    "question": question,
                    "answer": answer,
                    "score": score,
                    "evaluation": evaluation
                })
                total_score += score if score else 0

            candidate_record = {
                "name": name,
                "evaluations": evaluations,
                "total_score": total_score,
                "average_score": total_score / len(questions_list)
            }

            st.session_state.candidates.append(candidate_record)
            st.success("Your answers have been submitted and evaluated!")

            # Refresh button to clear answers
            if st.button("Refresh Answers"):
                st.session_state.candidates.clear()
                st.experimental_rerun()

# Admin Page
elif page == "Admin":
    st.subheader("Admin Page")
    
    # Check if candidates exist
    if st.session_state.candidates:
        # Create a dataframe from the candidates list
        data = {
            "Name": [c["name"] for c in st.session_state.candidates],
            "Total Score": [c["total_score"] for c in st.session_state.candidates],
            "Average Score": [round(c["average_score"], 2) for c in st.session_state.candidates]
        }
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Shortlist Top 3 Candidates
        if st.button("Shortlist Top 3 Candidates"):
            top_candidates = sorted(st.session_state.candidates, key=lambda x: x["total_score"], reverse=True)[:3]
            st.subheader("Top 3 Shortlisted Candidates:")
            for idx, candidate in enumerate(top_candidates, start=1):
                st.write(f"**{idx}. {candidate['name']}** - Total Score: {candidate['total_score']}")

        # Option to download full data
        if st.button("Download All Candidate Data as CSV"):
            full_data = []
            for candidate in st.session_state.candidates:
                for eval in candidate["evaluations"]:
                    full_data.append({
                        "Name": candidate["name"],
                        "Question": eval["question"],
                        "Answer": eval["answer"],
                        "Score": eval["score"],
                        "Evaluation Feedback": eval["evaluation"],
                        "Total Score": candidate["total_score"],
                        "Average Score": round(candidate["average_score"], 2)
                    })
            full_df = pd.DataFrame(full_data)
            csv = full_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="candidates_evaluations.csv",
                mime="text/csv"
            )
    else:
        st.info("No candidates yet. Please submit responses or generate dummy candidates.")
