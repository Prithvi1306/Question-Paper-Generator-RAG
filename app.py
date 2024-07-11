import streamlit as st
import json
import base64
from qp_gen import *
from evaluation import *

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

if st.sidebar.button("New Chat", key='refresh'):
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
            f"Options", options_with_keys, key=f"mcq_{i}"
        )

    # Displaying Subjective Answer Questions
    st.header("Subjective Answer Questions")

    for i in range(5):
        saq_question = question_paper["Question Paper"]["Subjective Answer Questions"][i][f"Q{i+11}"]
        st.subheader(f"Q{i+11}: {saq_question}")
        st.session_state.responses["essay"][i] = {
            "student_response": st.text_area(f"Answer", key=f"subjective_{i}"),
            "question_id": f"Q{i+11}"
        }

    # Button to submit responses
    if st.button("Submit & Evaluate Responses"):
        # Save responses to JSON
        responses_json = json.dumps(st.session_state.responses, indent=4)
        with open("responses.json", "w") as f:
            f.write(responses_json)
        # st.success("Responses saved successfully!")

        # Perform evaluation
        evaluation_results = complete_evaluation(question_paper, st.session_state.responses)
        st.session_state.evaluation_results = evaluation_results

        # Save evaluation results to JSON
        eval_results_json = json.dumps(evaluation_results, indent=4)
        with open("evaluation_results.json", "w") as f:
            f.write(eval_results_json)

# # Displaying the evaluation results if available
# st.title("Evaluation Results")

# # Display MCQ evaluation results
# st.header("MCQ Evaluation Results")
# for result in evaluation_results["mcq_evaluation"]:
#     st.write(result)

# # Display Essay evaluation results
# st.header("Essay Evaluation Results")
# for report in evaluation_results["essay_evaluation_report"]:
#     st.subheader("Evaluation Report")
#     for key, value in report["Evaluation Report"].items():
#         st.write(f"{key}: {value['score']} - {value['comments']}")

# Streamlit app layout
# st.title("Evaluation Results")

# st.header("MCQ Evaluation")
# for result in evaluation_results["mcq_evaluation"]:
#     st.write(result)

# st.header("Essay Evaluation Reports")
# for report in evaluation_results["essay_evaluation_report"]:
#     evaluation_report = report["Evaluation Report"]
#     st.subheader("Evaluation Report")
#     for key, value in evaluation_report.items():
#         st.write(f"**{key}:**")
#         st.write(f"Score: {value['score']}")
#         st.write(f"Comments: {value['comments']}")
#         st.write("---")

# st.title("Evaluation Results")

# st.header("MCQ Evaluation")
# for result in evaluation_results["mcq_evaluation"]:
#     st.write(result)

# st.header("Essay Evaluation Reports")
# for report in evaluation_results["essay_evaluation_report"]:
#     evaluation_report = report["Evaluation Report"]
#     st.subheader("Evaluation Report")
#     for criterion, details in evaluation_report.items():
#         if isinstance(details, dict):
#             st.write(f"**{criterion}:**")
#             st.write(f"Score: {details['score']}")
#             st.write(f"Comments: {details['comments']}")
#         else:
#             st.write(f"**{criterion}:** {details}")
#         st.write("---")

# Streamlit app layout
# st.title("Evaluation Results")

# st.header("Evaluation Report")
# st.subheader("MCQ Evaluation")
# for result in evaluation_results["mcq_evaluation"]:
#     st.write(result)

# st.subheader("Essay Evaluation Reports")
# for idx, report in enumerate(evaluation_results["essay_evaluation_report"]):
#     st.write(f"Essay {idx + 1} Evaluation Report")
#     evaluation_report = report["Evaluation Report"]
#     for criterion, details in evaluation_report.items():
#         if isinstance(details, dict):
#             st.write(f"**{criterion}:**")
#             st.write(f"Score: {details['score']}")
#             st.write(f"Comments: {details['comments']}")
#         else:
#             st.write(f"**{criterion}:** {details}")
#         st.write("---")
#     st.write("----")

# Streamlit app layout
# st.title("Evaluation Results")

# st.header("Evaluation Report")

# st.subheader("MCQ Evaluation")
# for result in evaluation_results["mcq_evaluation"]:
#     st.write(result)

# st.subheader("Essay Evaluation Reports")
# for idx, report in enumerate(evaluation_results["essay_evaluation_report"]):
#     st.write(f"Essay {idx + 1} Evaluation Report")
#     evaluation_report = report["Evaluation Report"]
#     report_text = ""
#     for criterion, details in evaluation_report.items():
#         if isinstance(details, dict):
#             report_text += f"**{criterion}**:\n- Score: {details['score']}\n- Comments: {details['comments']}\n\n"
#         else:
#             report_text += f"**{criterion}**: {details}\n\n"
#     st.write(report_text)
#     st.write("----")

st.header("Evaluation Report")

st.subheader("MCQ Evaluation")
for result in evaluation_results["mcq_evaluation"]:
    st.write(result)

st.subheader("Essay Evaluation Reports")
for idx, report in enumerate(evaluation_results["essay_evaluation_report"]):
    st.write(f"Essay {idx + 1} Evaluation Report")
    evaluation_report = report["Evaluation Report"]
    report_text = ""
    for criterion, details in evaluation_report.items():
        if isinstance(details, dict):
            report_text += f"\n\n{criterion}:- Score: {details['score']}- Comments: {details['comments']}"
        else:
            report_text += f"\n\n{criterion}: {details}"
    st.write(report_text)
    st.write("----")