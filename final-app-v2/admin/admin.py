import streamlit as st

def admin_page():
    st.header("📋 Summary Table")

    if "all_candidates" not in st.session_state or not st.session_state["all_candidates"]:
        st.info("No candidate data available yet.")
        return

    # Build summary table
    summary_data = []
    for candidate in st.session_state["all_candidates"]:
        summary_data.append({
            "Candidate": candidate["name"],
            "Total Score": candidate["total_score"]
        })

    st.table(summary_data)

    # Detailed evaluations
    st.markdown("## 📝 Detailed Evaluations")

    for idx, candidate in enumerate(st.session_state["all_candidates"], start=1):
        st.subheader(f"{idx}. {candidate['name']}")

        for i, (question, answer, feedback, score) in enumerate(zip(
            candidate["questions"],
            candidate["answers"],
            candidate["feedbacks"],
            candidate["scores"]
        ), start=1):
            st.markdown(f"**Q{i}: {question}**")
            st.markdown(f"- **Answer:** {answer}")
            st.markdown(f"- **Evaluation:** {feedback}")
            st.markdown(f"- **Score:** {score}/10")
            st.markdown("---")

        st.markdown(f"**✅ Total Score: {candidate['total_score']}/50**")
        st.markdown("***")
