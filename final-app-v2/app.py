import openai
import streamlit as st
import random
import re
import pandas as pd

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Predefined questions
questions_list = [
    "Why do you want to work with us?",
    "What is your greatest strength?",
    "What do you know about our company?",
    "Where do you see yourself in 5 years?",
    "What are your salary expectations?"
]

# Dummy answers for random generation
dummy_answers = [
    "I am passionate about the work you do.",
    "My greatest strength is my problem-solving ability.",
    "You are a leader in the industry with a strong reputation.",
    "In 5 years, I see myself growing into a leadership role.",
    "I expect a fair and competitive salary aligned with my skills."
]

# Function to evaluate one answer
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
        score_match = re.search(r'(\d+)', evaluation)
        if score_match:
            return int(score_match.group(1)), evaluation
        else:
            return None, evaluation
    except Exception as e:
        return None, f"Error: {e}"

# Initialize session state
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Candidate Page", "Admin Page"])

if page == "Candidate Page":
    st.title("Candidate Interview Submission")

    name = st.text_input("Enter your Name")
    answers = {}

    for question in questions_list:
        answers[question] = st.text_area(question)

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

elif page == "Admin Page":
    st.title("Admin Panel - View and Shortlist Candidates")

    # Button to generate dummy candidates
    if st.button("Generate 10 Dummy Candidates"):
        for i in range(10):
            name = f"Candidate_{random.randint(1000, 9999)}"
            evaluations = []
            total_score = 0
            for question in questions_list:
                answer = random.choice(dummy_answers)
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
        st.success("Generated 10 dummy candidates!")

    # Display table of all candidates
    if st.session_state.candidates:
        data = {
            "Name": [c["name"] for c in st.session_state.candidates],
            "Total Score": [c["total_score"] for c in st.session_state.candidates],
            "Average Score": [round(c["average_score"], 2) for c in st.session_state.candidates]
        }
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Shortlist Top 3
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
