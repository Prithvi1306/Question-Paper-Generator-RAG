import streamlit as st
import json
import base64
from qp_gen import get_question_paper
from evaluation import complete_evaluation

# Load the logo image
with open("logo.png", "rb") as f:
    data = base64.b64encode(f.read()).decode("utf-8")
    st.sidebar.markdown(
        f"""
        <div style="display:table;margin-top:-20%;margin-left:0%;">
            <img src="data:image/png;base64,{data}" width="130" height="70">
        </div>
        """,
        unsafe_allow_html=True,
    )

st.sidebar.markdown("-----")

def start_new_chat():
    st.session_state.clear()
    st.rerun()

if st.sidebar.button("**Refresh**", key='refresh'):
    start_new_chat()

st.title("Question Paper Generator")

# Initialize or retrieve session state
if "question_paper" not in st.session_state:
    st.session_state.question_paper = None
if "responses" not in st.session_state:
    st.session_state.responses = {
        "mcq": [None] * 10,  # Assume 10 MCQs
        "essay": [None] * 5  # Assume 5 SAQs
    }
if "evaluation_results" not in st.session_state:
    st.session_state.evaluation_results = None

topic = st.text_input("Enter the topic for the question paper:")

if st.button("Generate Question Paper"):
    if topic:
        with st.spinner("Generating question paper..."):
            question_paper = get_question_paper(topic)
            st.session_state.question_paper = question_paper
            st.success("Question paper generated successfully!")

            # Reset responses in session state
            st.session_state.responses = {
                "mcq": [None] * 10,
                "essay": [None] * 5
            }
    else:
        st.error("Please enter a topic.")

# Displaying the question paper if available
if st.session_state.question_paper:
    question_paper = st.session_state.question_paper

    # Displaying MCQs
    st.header("Multiple Choice Questions (MCQs)")

    for i in range(10):
        mcq_question = list(question_paper["Question Paper"]["Multiple Choice Questions (MCQs)"][i].values())[0]
        mcq_options = question_paper["Question Paper"]["Multiple Choice Questions (MCQs)"][i]["Options"]
        options_with_keys = [f"{key}: {value}" for key, value in mcq_options.items()]
        st.subheader(f"Q{i+1}: {mcq_question}")
        st.session_state.responses["mcq"][i] = st.radio(
            f"Options for Q{i+1}", options_with_keys, key=f"mcq_{i}"
        )

    # Displaying Subjective Answer Questions
    st.header("Subjective Answer Questions")

    for i in range(5):
        saq_question = question_paper["Question Paper"]["Subjective Answer Questions"][i][f"Q{i+11}"]
        st.subheader(f"Q{i+11}: {saq_question}")
        st.session_state.responses["essay"][i] = {
            "student_response": st.text_area(f"Answer for Q{i+11}", key=f"subjective_{i}"),
            "question_id": f"Q{i+11}"
        }

    # Button to submit responses
    if st.button("Submit & Evaluate Responses"):
        # Perform evaluation
        with st.spinner("Evaluating responses..."):
            evaluation_results = complete_evaluation(question_paper, st.session_state.responses)
            st.session_state.evaluation_results = evaluation_results

# Displaying the evaluation results if available
if st.session_state.evaluation_results:
    evaluation_results = st.session_state.evaluation_results

    st.title("Evaluation Results")

    st.header("MCQ Evaluation")
    for result in evaluation_results["mcq_evaluation"]:
        st.write(result)

    st.header("Essay Evaluation Reports")
    for idx, report in enumerate(evaluation_results["essay_evaluation_report"]):
        st.write(f"Essay {idx + 1} Evaluation Report")
        evaluation_report = report["Evaluation Report"]
        report_text = ""
        for criterion, details in evaluation_report.items():
            if isinstance(details, dict):
                report_text += f"\n\n{criterion}:\n- Score: {details['score']}\n- Comments: {details['comments']}"
            else:
                report_text += f"\n\n{criterion}: {details}"
        st.write(report_text)
        st.write("----")
