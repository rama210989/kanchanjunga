import streamlit as st

def admin_page():
    st.header("📋 Summary Table")

    if "all_candidates" not in st.session_state or not st.session_state["all_candidates"]:
        st.info("No candidate data available yet.")
        return

    # Build summary table
    summary_data = []
    for candidate in st.session_state["all_candidates"]:
        name = candidate.get("name", "Unknown")
        total_score = candidate.get("total_score", 0)
        summary_data.append({
            "Candidate": name,
            "Total Score": total_score
        })

    st.table(summary_data)

    # Detailed evaluations
    st.markdown("## 📝 Detailed Evaluations")

    for idx, candidate in enumerate(st.session_state["all_candidates"], start=1):
        st.subheader(f"{idx}. {candidate.get('name', 'Unknown')}")

        questions = candidate.get("questions", [])
        answers = candidate.get("answers", [])
        feedbacks = candidate.get("feedbacks", [])
        scores = candidate.get("scores", [])

        for i in range(len(questions)):
            question = questions[i] if i < len(questions) else "N/A"
            answer = answers[i] if i < len(answers) else "N/A"
            feedback = feedbacks[i] if i < len(feedbacks) else "No feedback"
            score = scores[i] if i < len(scores) else 0

            st.markdown(f"**Q{i+1}: {question}**")
            st.markdown(f"- **Answer:** {answer}")
            st.markdown(f"- **Evaluation:** {feedback}")
            st.markdown(f"- **Score:** {score}/10")
            st.markdown("---")

        st.markdown(f"**✅ Total Score: {candidate.get('total_score', 0)}/50**")
        st.markdown("***")
