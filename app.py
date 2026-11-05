import json
import os
from datetime import datetime, timezone
from io import StringIO

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="AI Response Evaluation System",
    page_icon="🧪",
    layout="wide",
)

RUBRIC = {
    "Accuracy": "Is the response factually correct and free from unsupported claims?",
    "Relevance": "Does it directly address the user's request?",
    "Instruction Following": "Does it follow all explicit constraints and requested format?",
    "Clarity": "Is it understandable, organized, and appropriately concise?",
    "Completeness": "Does it cover the important parts of the request?",
    "Safety": "Does it avoid harmful, discriminatory, privacy-invasive, or otherwise unsafe guidance?",
}

SCORE_LABELS = {
    1: "Poor",
    2: "Weak",
    3: "Adequate",
    4: "Good",
    5: "Excellent",
}

def score_label(score):
    return SCORE_LABELS.get(int(score), "Not scored")

def weighted_score(scores):
    if not scores:
        return 0.0
    return round(sum(scores.values()) / len(scores), 2)

def load_examples():
    path = os.path.join(os.path.dirname(__file__), "data", "sample_cases.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return []

def init_state():
    defaults = {
        "evaluations": [],
        "case_title": "",
        "user_prompt": "",
        "response_a": "",
        "response_b": "",
        "notes": "",
        "evaluator": "",
        "category": "General",
        "scores_a": {k: 3 for k in RUBRIC},
        "scores_b": {k: 3 for k in RUBRIC},
        "winner": "Tie",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

st.title("🧪 AI Response Evaluation System")
st.caption("A practical portfolio project for evaluating AI-generated responses with a consistent rubric.")

with st.sidebar:
    st.header("Evaluation workspace")
    page = st.radio("Navigate", ["Evaluate responses", "Evaluation history", "Rubric & methodology", "About this project"])
    st.divider()
    st.caption("Portfolio demonstration · Version 1.0")
    st.caption("Evaluations are stored in this browser session only. Export your results to keep them.")

if page == "Evaluate responses":
    st.subheader("1. Evaluation context")
    examples = load_examples()
    example_names = ["Start with a blank evaluation"] + [x["title"] for x in examples]
    selected = st.selectbox("Load a practice case (optional)", example_names)

    if st.button("Load selected case", disabled=(selected == example_names[0])):
        example = next(x for x in examples if x["title"] == selected)
        st.session_state.case_title = example["title"]
        st.session_state.user_prompt = example["prompt"]
        st.session_state.response_a = example["response_a"]
        st.session_state.response_b = example["response_b"]
        st.session_state.category = example.get("category", "General")
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Case title", key="case_title", placeholder="e.g., Customer support refund policy")
        st.text_input("Evaluator name / ID", key="evaluator", placeholder="e.g., Evaluator 01")
    with col2:
        st.selectbox("Task category", ["General", "Question answering", "Customer support", "Summarization", "Translation", "Instruction following", "Safety"], key="category")
        st.caption("Use fictional or public examples. Do not enter private customer data.")

    st.text_area("User prompt", key="user_prompt", height=110, placeholder="Paste the original user request here.")

    st.subheader("2. Responses to evaluate")
    a_col, b_col = st.columns(2)
    with a_col:
        st.markdown("#### Response A")
        st.text_area("Response A content", key="response_a", height=220, placeholder="Paste AI response A...")
    with b_col:
        st.markdown("#### Response B")
        st.text_area("Response B content", key="response_b", height=220, placeholder="Paste AI response B...")

    st.subheader("3. Score each response")
    st.caption("Use the same standards for both responses. A score of 1 is poor; 5 is excellent.")
    for criterion, description in RUBRIC.items():
        st.markdown(f"**{criterion}**")
        st.caption(description)
        left, right = st.columns(2)
        with left:
            st.select_slider(
                f"{criterion} — A",
                options=[1, 2, 3, 4, 5],
                value=st.session_state.scores_a[criterion],
                format_func=lambda x: f"{x} — {score_label(x)}",
                key=f"slider_a_{criterion}",
            )
        with right:
            st.select_slider(
                f"{criterion} — B",
                options=[1, 2, 3, 4, 5],
                value=st.session_state.scores_b[criterion],
                format_func=lambda x: f"{x} — {score_label(x)}",
                key=f"slider_b_{criterion}",
            )

    st.subheader("4. Comparative judgment")
    st.radio("Which response is better overall?", ["Response A", "Response B", "Tie"], horizontal=True, key="winner")
    st.text_area("Evidence and evaluator notes", key="notes", height=110,
                 placeholder="Explain the most important strengths, weaknesses, and evidence supporting your decision.")

    scores_a = {k: int(st.session_state.get(f"slider_a_{k}", 3)) for k in RUBRIC}
    scores_b = {k: int(st.session_state.get(f"slider_b_{k}", 3)) for k in RUBRIC}
    avg_a, avg_b = weighted_score(scores_a), weighted_score(scores_b)

    st.subheader("5. Live score summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Response A average", f"{avg_a}/5")
    m2.metric("Response B average", f"{avg_b}/5")
    m3.metric("Score difference (A − B)", f"{avg_a - avg_b:+.2f}")

    missing = []
    if not st.session_state.user_prompt.strip():
        missing.append("user prompt")
    if not st.session_state.response_a.strip():
        missing.append("response A")
    if not st.session_state.response_b.strip():
        missing.append("response B")

    if missing:
        st.info("Complete the following before saving: " + ", ".join(missing) + ".")
    if st.button("Save evaluation", type="primary", disabled=bool(missing)):
        record = {
            "evaluation_id": f"EVAL-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{len(st.session_state.evaluations)+1:03d}",
            "created_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "case_title": st.session_state.case_title.strip() or "Untitled evaluation",
            "evaluator": st.session_state.evaluator.strip() or "Not specified",
            "category": st.session_state.category,
            "prompt": st.session_state.user_prompt,
            "response_a": st.session_state.response_a,
            "response_b": st.session_state.response_b,
            "scores_a": scores_a,
            "scores_b": scores_b,
            "average_a": avg_a,
            "average_b": avg_b,
            "winner": st.session_state.winner,
            "notes": st.session_state.notes,
        }
        st.session_state.evaluations.append(record)
        st.success(f"Saved {record['evaluation_id']}. Open Evaluation history to review or export it.")

elif page == "Evaluation history":
    st.subheader("Saved evaluations")
    records = st.session_state.evaluations
    if not records:
        st.info("No evaluations saved in this session yet. Complete an evaluation first.")
    else:
        summary = pd.DataFrame([{
            "Evaluation ID": r["evaluation_id"],
            "Date (UTC)": r["created_at_utc"],
            "Case": r["case_title"],
            "Category": r["category"],
            "Response A": r["average_a"],
            "Response B": r["average_b"],
            "Preferred": r["winner"],
            "Evaluator": r["evaluator"],
        } for r in records])
        st.dataframe(summary, use_container_width=True, hide_index=True)

        export_rows = []
        for r in records:
            row = {
                "evaluation_id": r["evaluation_id"],
                "created_at_utc": r["created_at_utc"],
                "case_title": r["case_title"],
                "category": r["category"],
                "evaluator": r["evaluator"],
                "prompt": r["prompt"],
                "response_a": r["response_a"],
                "response_b": r["response_b"],
                "average_a": r["average_a"],
                "average_b": r["average_b"],
                "winner": r["winner"],
                "notes": r["notes"],
            }
            for criterion in RUBRIC:
                row[f"A_{criterion.lower().replace(' ', '_')}"] = r["scores_a"][criterion]
                row[f"B_{criterion.lower().replace(' ', '_')}"] = r["scores_b"][criterion]
            export_rows.append(row)
        csv_data = pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8-sig")
        st.download_button("Download evaluations as CSV", csv_data, "ai_response_evaluations.csv", "text/csv")
        json_data = json.dumps(records, ensure_ascii=False, indent=2).encode("utf-8")
        st.download_button("Download evaluations as JSON", json_data, "ai_response_evaluations.json", "application/json")

        selected_id = st.selectbox("Inspect an evaluation", [r["evaluation_id"] for r in records])
        record = next(r for r in records if r["evaluation_id"] == selected_id)
        with st.expander("View full evaluation", expanded=True):
            st.write("**Prompt:**", record["prompt"])
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Response A**")
                st.write(record["response_a"])
                st.write("Scores:", record["scores_a"])
            with c2:
                st.markdown("**Response B**")
                st.write(record["response_b"])
                st.write("Scores:", record["scores_b"])
            st.write("**Preferred:**", record["winner"])
            st.write("**Notes:**", record["notes"])

elif page == "Rubric & methodology":
    st.subheader("Evaluation rubric")
    st.write("Each response is scored independently across six dimensions on a 1–5 scale.")
    rubric_df = pd.DataFrame([
        {"Criterion": k, "What to assess": v, "1": "Poor", "3": "Adequate", "5": "Excellent"}
        for k, v in RUBRIC.items()
    ])
    st.dataframe(rubric_df, use_container_width=True, hide_index=True)
    st.markdown("""
    **Scoring guidance**
    - **1 — Poor:** Major issues; the response fails this dimension.
    - **2 — Weak:** Noticeable issues that reduce usefulness.
    - **3 — Adequate:** Acceptable, but has clear room for improvement.
    - **4 — Good:** Strong performance with only minor issues.
    - **5 — Excellent:** Fully meets the criterion with no meaningful issue.

    **Recommended evaluation workflow**
    1. Read the user prompt and identify its explicit requirements.
    2. Read each response independently before comparing them.
    3. Score each response against the same rubric.
    4. Record specific evidence, not just personal preference.
    5. Select the stronger response or mark a tie.
    6. Review the scores and notes for consistency before submitting.

    **Important:** The average is a descriptive aid, not an automatic truth score. A serious safety or factual error may outweigh a small numerical advantage.
    """)

elif page == "About this project":
    st.subheader("Project overview")
    st.markdown("""
    **AI Response Evaluation System** is a portfolio demonstration of a structured human-evaluation workflow for AI-generated text.

    It allows an evaluator to:
    - compare two AI responses to the same prompt;
    - score them against a consistent six-dimension rubric;
    - document evidence and a comparative judgment;
    - review saved evaluations during the current session;
    - export records to CSV or JSON for further analysis.

    **Intended demonstration:** AI evaluation, analytical thinking, instruction following, quality assurance, written communication, and documentation.

    **Limitations:** This is an educational portfolio tool, not an official evaluation platform and not a substitute for client-specific guidelines. Data is kept in Streamlit session memory and may be lost when the session ends; export records to preserve them.
    """)
    st.info("All sample cases are fictional and intended for practice.")

st.divider()
st.caption("Built as an educational portfolio project. Always follow the evaluation guidelines supplied by the hiring organization.")
