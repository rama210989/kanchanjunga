import streamlit as st
import pandas as pd

def admin_page():
    st.header("📋 Summary Table")

    if "all_candidates" not in st.session_state or len(st.session_state["all_candidates"]) == 0:
        st.info("No candidates submitted yet.")
        return

    # Summary Table
    summary_data = [{
        "Candidate": c["name"],
        "Total Score": c["total_score"]
    } for c in st.session_state["all_candidates"]]
    st.dataframe(pd.DataFrame(summary_data))

    st.markdown("### 📝 Detailed Evaluations")
    for idx, candidate in enumerate(st.session_state["all_candidates"], start=1):
        st.markdown(f"**{idx}. {candidate['name']}**")
        for i in range(len(candidate["questions"])):
            st.markdown(f"""
**Q{i+1}: {candidate['questions'][i]}**

**Answer:** {candidate['answers'][i]}

**Evaluation:** {candidate['feedbacks'][i]}

**Score:** {candidate['scores'][i]}/10
""")
        st.markdown(f"✅ **Total Score: {candidate['total_score']}/50**")
