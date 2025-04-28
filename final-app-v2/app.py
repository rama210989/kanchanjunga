import openai
import streamlit as st
import pandas as pd
import random
import os
import re
import csv

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# List of predefined questions
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
        score_match = re.search(r'(\d+)', evaluation)
        if score_match:
            return int(score_match.group(1)), evaluation
        else:
            return None, evaluation
    except Exception as e:
        return None, f"Error evaluating answer: {e}"

# Streamlit UI components
st.title("Interview Question Evaluator")

# Initialize session state if not present
if "evaluated_candidates" not in st.session_state:
    st.session_state.evaluated_candidates = []

# CSV Upload for Admin
uploaded_file = st.file_uploader("Upload a CSV of Candidate Answers", type=["csv"])

if uploaded_file:
    try:
        # Read CSV file
        data = pd.read_csv(uploaded_file)
        st.session_state.candidates = data
    except Exception as e:
        st.error(f"Error reading the CSV file: {e}")

# Candidate page for responses
st.subheader("Candidate Page")

candidate_name = st.text_input("Enter your name:")

# Store responses for candidates
if candidate_name:
    answers = {}
    for question in questions_list:
        answers[question] = st.text_area(question)

    # Button to evaluate candidate's responses
    if st.button("Submit Answers"):
        total_score = 0
        evaluations = []

        for question in questions_list:
            answer = answers[question]
            if answer:
                score, evaluation = evaluate_answer(question, answer)
                if score is not None:
                    evaluations.append(score)
                    total_score += score
                st.write(f"Evaluation for '{question}': {evaluation}")

        # Calculate the average score and percentage
        if evaluations:
            average_score = total_score / len(evaluations)
            percentage = (average_score / 10) * 100
            st.write(f"Average Evaluation Score: {average_score}/10")
            st.write(f"Percentage: {percentage:.2f}%")

            # Save evaluated candidate to session state
            st.session_state.evaluated_candidates.append({
                "name": candidate_name,
                "score": total_score,
                "percentage": percentage,
                "answers": answers
            })

            # Reset form after submission
            st.session_state.candidate_name = ""
            for question in questions_list:
                st.session_state[question] = ""

# Admin page
st.subheader("Admin Page")

# Show all candidates' evaluations
if len(st.session_state.evaluated_candidates) > 0:
    st.write("Evaluated Candidates:")

    # Display candidate evaluations
    for candidate in st.session_state.evaluated_candidates:
        st.write(f"**Name**: {candidate['name']}")
        st.write(f"**Score**: {candidate['score']}")
        st.write(f"**Percentage**: {candidate['percentage']:.2f}%")
        st.write("**Answers and Evaluations:**")
        
        for i, question in enumerate(questions_list):
            answer = candidate["answers"].get(question, "No answer")
            score, evaluation = evaluate_answer(question, answer)
            st.write(f"**{question}:** {answer}")
            st.write(f"Evaluation: {evaluation}")
            st.write(f"Score: {score}/10")
        st.write("---")

# Option to upload CSV file with candidates' answers for admin
if uploaded_file:
    st.session_state.evaluated_candidates = []  # Clear previously evaluated candidates
    # Process new candidates from the uploaded file and evaluate them
    for index, row in st.session_state.candidates.iterrows():
        total_score = 0
        evaluations = []
        candidate_answers = row[1:].to_dict()
        for question, answer in candidate_answers.items():
            score, evaluation = evaluate_answer(question, answer)
            if score is not None:
                evaluations.append(score)
                total_score += score

        average_score = total_score / len(evaluations)
        percentage = (average_score / 10) * 100

        st.session_state.evaluated_candidates.append({
            "name": row["Name"],
            "score": total_score,
            "percentage": percentage,
            "answers": candidate_answers
        })

        # Show evaluated candidate
        st.write(f"**Name**: {row['Name']}")
        st.write(f"**Score**: {total_score}")
        st.write(f"**Percentage**: {percentage:.2f}%")
        st.write("**Answers and Evaluations:**")
        for question, answer in candidate_answers.items():
            score, evaluation = evaluate_answer(question, answer)
            st.write(f"**{question}:** {answer}")
            st.write(f"Evaluation: {evaluation}")
            st.write(f"Score: {score}/10")
        st.write("---")

    # Display top 3 candidates based on score
    st.write("Top 3 Candidates:")
    top_3 = sorted(st.session_state.evaluated_candidates, key=lambda x: x['score'], reverse=True)[:3]
    for candidate in top_3:
        st.write(f"**Name**: {candidate['name']}")
        st.write(f"**Score**: {candidate['score']}")
        st.write(f"**Percentage**: {candidate['percentage']:.2f}%")
