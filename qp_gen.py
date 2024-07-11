import dotenv
import json
import os
from langchain_openai import ChatOpenAI
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
from json_structures import *
from prompts import *

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

llm = ChatOpenAI(temperature=0.6, model="gpt-3.5-turbo")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

chroma_collection_name = "science2_indexes"
persistent_client = chromadb.PersistentClient(path=r"C:\Prithvi\Proj\chromadb\indexes")
collection = persistent_client.get_or_create_collection(chroma_collection_name)
vector_store = Chroma(
    client=persistent_client,
    collection_name=chroma_collection_name,
    embedding_function=embeddings,
)

db = vector_store.as_retriever(search_type="similarity")

prompt_template = qp_generation_template

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

prompt = PromptTemplate.from_template(template=prompt_template)

rag_chain = (
    {"context": db | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    |StrOutputParser()
    )

qp_structure = qp_structure

def jsonConvertor(context, jsonStructure):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""{context} Convert the above in the JSON structure like {jsonStructure}"""
    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        temperature = 0,
        messages=[{"role": "system", "content": "You are a helpful assistant who creates JSON structure."},
                    {"role": "user", "content": f"{prompt}"}]
        )
    summary = response.choices[0].message.content
    return summary

def write_json_to_file(data):
    filename = 'question_paper.json'
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        # print(f"Data successfully written to {filename}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

def get_question_paper(topic):
    response = rag_chain.invoke(topic)
    qp_json = jsonConvertor(response,qp_structure)
    json_res = json.loads(qp_json)
    write_json_to_file(json_res)
    return json_res