import streamlit as st

def admin_page():
    st.title("🧠 Admin Panel: Evaluations")

    if "all_candidates" not in st.session_state or not st.session_state["all_candidates"]:
        st.info("No candidate data submitted yet.")
        return

    # Summary Table
    st.header("📋 Summary Table")
    summary_data = [
        {"Candidate": c["name"], "Total Score": c["score"]}
        for c in st.session_state["all_candidates"]
    ]
    st.table(summary_data)

    # Detailed Evaluations
    st.header("📝 Detailed Evaluations")
    for idx, candidate in enumerate(st.session_state["all_candidates"], 1):
        st.subheader(f"{idx}. {candidate['name']}")
        for i, feedback in enumerate(candidate["feedback"]):
            st.write(f"Q{i+1}: {feedback}")
        st.markdown(f"**Total Score:** {candidate['score']}/50")
        st.markdown("---")
