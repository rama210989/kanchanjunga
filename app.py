import streamlit as st
import openai

# Streamlit page setup
st.set_page_config(page_title="Interview Chatbot", layout="wide")
st.title("🧠 AI Interview Evaluator")

# API Key Input (or use Streamlit secrets later)
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Interview Questions
questions = [
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

# Collect User Responses
st.subheader("💬 Please answer the following questions:")

responses = {}
for idx, question in enumerate(questions):
    answer = st.text_area(f"{idx+1}. {question}", key=f"q{idx}")
    responses[question] = answer

# Evaluation function
def evaluate_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\n\nEvaluate this response on a scale of 1 to 10 and explain why."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response['choices'][0]['message']['content']

# Button to Submit and Evaluate
if st.button("🚀 Submit and Get Evaluation"):
    st.subheader("📊 Evaluation Results:")
    for question, answer in responses.items():
        if answer.strip() != "":
            with st.spinner(f"Evaluating: {question}"):
                evaluation = evaluate_answer(question, answer)
                st.markdown(f"**Question:** {question}")
                st.markdown(f"**Your Answer:** {answer}")
                st.success(f"**Evaluation:** {evaluation}")
                st.markdown("---")
        else:
            st.warning(f"Skipped: {question}")
