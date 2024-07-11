import dotenv
import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from prompts import *
from json_structures import *
from qp_gen import * 

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(temperature=0.2, model="gpt-3.5-turbo")

summarization_prompt = summarization_template

# Define the initial prompt to summarize the context into key points
summarize_prompt_template = ChatPromptTemplate.from_template(summarization_prompt)

# Create the LLMChain for summarizing the context into key points
key_points_chain = LLMChain(llm=llm, prompt=summarize_prompt_template, output_key='key_points')

# Define the evaluation prompt template
eval_prompt_template = evaluation_template

# Create the PromptTemplate for the evaluation
eval_prompt = ChatPromptTemplate.from_template(eval_prompt_template)

# Create the LLMChain for the evaluation
eval_chain = LLMChain(llm=llm, prompt=eval_prompt, output_key = "evaluation_report" )

# Create the SequentialChain
overall_chain = SequentialChain(
    chains=[key_points_chain, eval_chain],
    input_variables=["context", "student_response"],
    output_variables=["evaluation_report"]
)

def load_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def extract_model_answers(question_paper):
    # saq = question_paper['Question Paper']['Short Answer Questions']
    # laq = question_paper['Question Paper']['Long Answer Questions']
    model_answers = question_paper['Question Paper']['Subjective Answer Questions']
    return model_answers

def check_mcq_responses(question_paper, response):
    student_responses = response
    mcqs = question_paper["Question Paper"]["Multiple Choice Questions (MCQs)"]
    correct_options = []
    mcq_evalaution = []

    # Extract correct options and explanations
    for q in mcqs:
        correct_options.append(q["Correct Option"])

    # Compare student responses with correct options
    for i, answer in enumerate(student_responses['mcq']):
        if answer[0] == correct_options[i]:
            mcq_evalaution.append(f"Q{i+1}: Correct. You chose '{answer[0]}', Which is the correct option.")
        else:
            mcq_evalaution.append(f"Q{i+1}: Incorrect. You chose '{answer[0]}', correct option was '{correct_options[i]}")

    return mcq_evalaution

def evaluation_chain(context, student_response):
    # result = overall_chain.invoke(context=context, student_response=student_response)
    result = overall_chain.invoke({"context": context, "student_response": student_response})
    evaluation_score = jsonConvertor(result, evalualtion_json_structure)
    evaluation_json = json.loads(evaluation_score)
    return evaluation_json

def essay_evaluation(question_paper, student_responses):
    student_response = student_responses['essay']
    model_answers = extract_model_answers(question_paper)
    complete_evaluation_report = []
    for i in range(len(student_response)):
        eval_report = evaluation_chain(model_answers[i]["Answer"], student_response[i]['student_response'])
        complete_evaluation_report.append(eval_report)
    return complete_evaluation_report

def complete_evaluation(question_paper, response):
    mcq_evaluation = check_mcq_responses(question_paper, response)
    essay_evaluation_report = essay_evaluation(question_paper, response)
    full_evaluation_report = {"mcq_evaluation": mcq_evaluation, 
                              "essay_evaluation_report": essay_evaluation_report}
    return full_evaluation_report