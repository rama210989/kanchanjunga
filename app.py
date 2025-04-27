import openai
import streamlit as st

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# List of 10 predefined questions
questions_list = [
    "Tell me about yourself.",
    "Why do you want to work with us?",
    "What is your greatest strength?",
    "What is your biggest weakness?",
    "Describe a challenging situation you faced and how you overcame it.",
    "How do you prioritize tasks when working on multiple projects?",
    "What do you know about our company?",
    "Where do you see yourself in 5 years?",
    "Why should we hire you?",
    "What are your salary expectations?"
]

# Function to evaluate the answer
def evaluate_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\n\nEvaluate this response on a scale of 1 to 10 and explain why."
    try:
        # Using the new OpenAI API (chat-based, version >=1.0.0)
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can also try gpt-3.5-turbo based on availability
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  # Adjust token limit based on answer length
            temperature=0.7
        )
        # Return the evaluation result
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        # Return any errors encountered
        return f"Error evaluating answer: {e}"

# Streamlit UI components
st.title("Interview Question Evaluator")

# Select a question from the predefined list
question = st.selectbox("Choose a question", questions_list)

# Input field for answer
answer = st.text_area("Enter your answer:")

# Button to evaluate the answer
if st.button("Evaluate Answer"):
    if answer:
        evaluation = evaluate_answer(question, answer)
        st.write("Evaluation:")
        st.write(evaluation)
    else:
        st.write("Please enter an answer.")
