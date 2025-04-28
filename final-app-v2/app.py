import openai
import streamlit as st
import pandas as pd
import re

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
        # Using gpt-3.5-turbo model with the chat-based API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are an AI that evaluates interview answers on a scale of 1 to 10."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Adjust token limit based on answer length
            temperature=0.7
        )
        # Extract the evaluation text
        evaluation = response['choices'][0]['message']['content'].strip()

        # Use regular expression to extract a score between 1 and 10
        score_match = re.search(r'(\d+)', evaluation)
        if score_match:
            return int(score_match.group(1)), evaluation  # Return both score and explanation
        else:
            return None, evaluation  # If no score is found
    except Exception as e:
        # Return any errors encountered
        return None, f"Error evaluating answer: {e}"

# Streamlit UI components
st.title("Interview Question Evaluator")

# Define pages for candidate and admin
PAGES = ["Candidate Page", "Admin Page"]
page = st.sidebar.selectbox("Select Page", PAGES)

# Candidate Page
if page == "Candidate Page":
    st.header("Candidate Interview Form")

    candidate_name = st.text_input("Enter your Name", "")
    answers = {}

    for question in questions_list:
        answers[question] = st.text_area(question)

    if st.button("Submit Answers"):
        if candidate_name and all(answers.values()):
            total_score = 0
            evaluations = []
            for question in questions_list:
                answer = answers[question]
                score, evaluation = evaluate_answer(question, answer)
                if score is not None:
                    evaluations.append(score)
                    total_score += score
                st.write(f"Evaluation for '{question}': {evaluation}")

            average_score = total_score / len(evaluations) if evaluations else 0
            percentage = (average_score / 10) * 100  # Convert to percentage (out of 10)

            st.write(f"Total Score: {total_score}/50")
            st.write(f"Average Evaluation Score: {average_score}/10")
            st.write(f"Percentage: {percentage:.2f}%")

            # Store responses in session_state for admin
            if "candidates" not in st.session_state:
                st.session_state.candidates = []

            st.session_state.candidates.append({
                "name": candidate_name,
                "answers": answers,
                "score": total_score,
                "average_score": average_score,
                "percentage": percentage
            })

            st.success("Your responses have been submitted and evaluated!")

    # Refresh button to clear the inputs
    if st.button("Clear Responses"):
        st.experimental_rerun()

# Admin Page
elif page == "Admin Page":
    st.header("Admin - Candidate Evaluations")

    # Option to upload CSV
    uploaded_file = st.file_uploader("Upload CSV file with candidate responses", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Ensure the CSV has the necessary columns (Name and Answers)
        required_columns = ["Name", "Answer 1", "Answer 2", "Answer 3", "Answer 4", "Answer 5"]
        if not all(col in df.columns for col in required_columns):
            st.error("CSV must contain columns: Name, Answer 1, Answer 2, Answer 3, Answer 4, Answer 5.")
        else:
            st.write(df)

            # Evaluate the uploaded responses
            total_score = 0
            evaluations = []
            for index, row in df.iterrows():
                candidate_name = row["Name"]
                st.write(f"Evaluating {candidate_name}'s Responses:")

                candidate_scores = []
                for i, question in enumerate(questions_list):
                    answer = row[f"Answer {i + 1}"]
                    score, evaluation = evaluate_answer(question, answer)
                    if score is not None:
                        candidate_scores.append(score)
                        st.write(f"Question: {question}")
                        st.write(f"Answer: {answer}")
                        st.write(f"Evaluation: {evaluation}")
                        st.write(f"Score: {score}")

                candidate_total_score = sum(candidate_scores)
                candidate_average_score = candidate_total_score / len(candidate_scores) if candidate_scores else 0
                candidate_percentage = (candidate_average_score / 10) * 100  # Convert to percentage

                total_score += candidate_total_score
                evaluations.append({
                    "Name": candidate_name,
                    "Total Score": candidate_total_score,
                    "Average Score": candidate_average_score,
                    "Percentage": candidate_percentage
                })

            # Display the evaluation results
            result_df = pd.DataFrame(evaluations)
            st.write("Evaluation Results:")
            st.write(result_df)

            # Shortlist the top 3 candidates
            top_candidates = result_df.sort_values(by="Total Score", ascending=False).head(3)
            st.write("Top 3 Candidates Shortlisted:")
            st.write(top_candidates)

    else:
        st.write("Upload a CSV to evaluate multiple candidates.")
        
    # Alternatively, you can view the candidates evaluated so far in session_state
    if "candidates" in st.session_state:
        st.write("Candidates Evaluated So Far:")
        st.write(pd.DataFrame(st.session_state.candidates))

        # Shortlist top 3 based on scores from session_state
        top_candidates_session = sorted(st.session_state.candidates, key=lambda x: x["score"], reverse=True)[:3]
        st.write("Top 3 Candidates Shortlisted from Session:")
        st.write(pd.DataFrame(top_candidates_session))
