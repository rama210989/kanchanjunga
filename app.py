import openai
import streamlit as st

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
        # Using the old OpenAI API (completion-based, version == 0.28)
        response = openai.Completion.create(
            model="text-davinci-003",  # Using text-davinci-003 since it is supported in 0.28
            prompt=prompt,
            max_tokens=150,  # Adjust token limit based on answer length
            temperature=0.7
        )
        # Return the evaluation result
        return response['choices'][0]['text'].strip()
    except Exception as e:
        # Return any errors encountered
        return f"Error evaluating answer: {e}"

# Streamlit UI components
st.title("Interview Question Evaluator")

# Dictionary to store answers
answers = {}

# Loop over the questions and create input fields
for question in questions_list:
    answers[question] = st.text_area(question)

# Button to evaluate the answers
if st.button("Evaluate Answers"):
    total_score = 0
    evaluations = []

    # Evaluate each answer and calculate the total score
    for question in questions_list:
        answer = answers[question]
        if answer:
            evaluation = evaluate_answer(question, answer)
            # Try to extract a score from the evaluation response
            try:
                score = int(evaluation.split()[0])  # Assume the first number in the evaluation is the score
                evaluations.append(score)
                total_score += score
            except ValueError:
                st.write(f"Could not extract a valid score for question: '{question}'")
                evaluations.append(0)

    # Calculate the average score
    if evaluations:
        average_score = total_score / len(evaluations)
        percentage = (average_score / 10) * 100  # Convert to percentage (out of 10)
        st.write(f"Average Evaluation Score: {average_score}/10")
        st.write(f"Percentage: {percentage:.2f}%")
    else:
        st.write("Please provide answers to all questions.")

