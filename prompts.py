qp_generation_template = """
Your task involves the following steps:

1. Understand the requirements based on the {question} and generate a question paper in the provided format.
2. Use the {context} to create a question paper and its answers as per the rules.
3. Provide the correct option for the MCQs and model answers for short answer questions and long answer questions.

Please adhere to these critical rules:
<rules>
1) Ensure the question paper contains exactly 15 questions.
2) Structure the paper with 10 MCQs, 5 Subjective Answer Questions (minimum 100 words).
3) Always provide the correct option for MCQs.
4) Maintain relevance and context in all questions.
5) The question paper should have unique IDs in the format question+n as shown in e.g., question1.
6) Always use the keys: Question Paper, Multiple Choice Questions (MCQs), Subjective Answer Questions.
7) Ensure that the keys in the question paper structure remain consistent.
8) Never issue an empty question paper,If the question is out of the context please you you donot know
</rules>

Follow the below structure for the question paper:

Question Paper:

Multiple Choice Questions (MCQs):
   Q1: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
   
   Q2: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
   
   Q3: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
   
   Q4: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
    
   Q5: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option:  

   Q6: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
   
   Q7: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
   
   Q8: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
   
   Q9: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option: 
    
   Q10: 
   Options:
     A. 
     B. 
     C. 
     D. 
   Correct Option:  

Subjective Answer Questions:
   ID:
   Q11:  
   Answer: 

   ID: 
   Q12:
   Answer: 

   ID: 
   Q13:
   Answer: 

   ID:
   Q14:  
   Answer:

   ID:
   Q15:  
   Answer: 
   
"""

evaluation_template = """
Based on the provided key points: {key_points}
And the student's response: "{student_response}"

Follow these guidelines to generate the evaluation report:

1. Use Clear Headings: Each section of the report should have a heading: Coverage, Depth, Clarity, Relevance, Overall Quality, Additional Comments.
2. Rate on a 1-5 Scale: For each section, provide a rating from 1 to 5 (1 being the lowest, 5 being the highest).
3. Justify Each Rating: Give a short and specific justification for each rating, referencing specific parts of the student's response.
4. Be Concise: Use clear, concise language for all comments.
5. Organize Well: Ensure the report is well-organized and easy to read.
6. Display Overall Score at the End: Show the overall score at the end of the report in the format "Score: X.X/5".

Evaluation Criteria:

Coverage:
   - Rating: (1-5)
   - Justification: Evaluate how thoroughly the response covers the key points provided.

Depth:
   - Rating: (1-5)
   - Justification: Assess the level of detail and insight in the response, including analysis, explanations, and examples.

Clarity:
   - Rating: (1-5)
   - Justification: Comment on the organization, coherence, and readability of the response.

Relevance:
   - Rating: (1-5)
   - Justification: Determine how well the response stays on topic and directly addresses the question or prompt.

Overall Quality:
   - Rating: (1-5)
   - Justification: Provide an overall assessment of the response, summarizing strengths and areas for improvement.

Example Format for the Report:

Evaluation Report

Coverage: 2/5
   The response does not address the key points provided, instead discussing the impact of technology on communication.

Depth: 3/5
   The analysis is relatively detailed but lacks examples.

Clarity: 5/5
   The response is very clear and well-organized.

Relevance: 1/5
   The response is not relevant to the prompt.

Overall Quality: 2/5
   Despite being well-written, the response is not relevant and does not cover the key points provided.

Score: 2.6/5
"""
summarization_template = """Summarize the following {context} into key points:\n"""