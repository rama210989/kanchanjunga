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

        # Extract score using regular expression
        score_match = re.search(r'(\d+)', evaluation)
        if score_match:
            return int(score_match.group(1)), evaluation
        else:
            return None, evaluation
    except Exception as e:
        return None, f"Error evaluating answer: {e}"

# Initialize candidate list in session_state
if "candidates" not in st.session_state:
    st.session_state.candidates = []

# Streamlit UI
st.title("Interview Question Evaluator - Final Version")

# Candidate Name (mandatory)
candidate_name = st.text_input("Enter your full name:")

# Dictionary to store answers
answers = {}

# Display questions
for question in questions_list:
    answers[question] = st.text_area(question)

# Submit button
if st.button("Submit Answers"):
    if not candidate_name.strip():
        st.warning("Please enter your name before submitting!")
    else:
        total_score = 0
        evaluations = []
        all_scores = []

        # Evaluate each answer
        for question in questions_list:
            answer = answers[question]
            if answer.strip():
                score, evaluation = evaluate_answer(question, answer)
                if score is not None:
                    evaluations.append((question, evaluation))
                    all_scores.append(score)
                    total_score += score
                else:
                    evaluations.append((question, "Could not evaluate."))

        # After evaluating all
        if all_scores:
            average_score = total_score / len(all_scores)
            percentage = (average_score / 10) * 100

            # Show evaluations
            st.subheader("Evaluation Results:")
            for question, evaluation in evaluations:
                st.write(f"**{question}**: {evaluation}")

            st.write(f"**Total Score:** {total_score}")
            st.write(f"**Average Score:** {average_score:.2f}/10 ({percentage:.2f}%)")

            # Save candidate details
            st.session_state.candidates.append({
                "Name": candidate_name,
                "Total Score": total_score,
                "Average Score": average_score
            })

            st.success("Your answers have been submitted successfully!")
        else:
            st.warning("Please provide answers to all questions.")

st.markdown("---")

# Admin section
st.subheader("Admin Section - View Top 3 Candidates")
if st.button("Show Results"):
    if st.session_state.candidates:
        df = pd.DataFrame(st.session_state.candidates)
        df_sorted = df.sort_values(by="Average Score", ascending=False)

        st.write("### All Candidates:")
        st.dataframe(df_sorted)

        st.write("### Top 3 Candidates:")
        st.dataframe(df_sorted.head(3))
    else:
        st.info("No candidate submissions yet.")
