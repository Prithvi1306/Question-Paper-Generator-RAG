import os
import chromadb
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyMuPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import dotenv

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

def create_chunks(directory_path):
    loader = DirectoryLoader(directory_path, glob="./*.pdf", loader_cls=PyMuPDFLoader)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100, add_start_index=True)
    documents = loader.load_and_split(text_splitter=text_splitter)
    chunked_data = text_splitter.split_documents(documents)    
    return chunked_data

chroma_collection_name = "science2_indexes"
persistent_client = chromadb.PersistentClient(path=r"C:\Prithvi\Proj\chromadb\indexes")
collection = persistent_client.get_or_create_collection(chroma_collection_name)
vector_db = Chroma(
    client=persistent_client,
    collection_name=chroma_collection_name,
    embedding_function=embeddings,
)

final_docs = create_chunks(r"C:\Prithvi\Proj\10th science")
vector_db.add_documents(final_docs)