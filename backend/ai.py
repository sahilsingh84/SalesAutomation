import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Constants
EMBEDDING_MODEL = "models/embedding-001"
PDF_DIRECTORY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "files")
FAISS_INDEX_NAME = os.path.join(os.path.dirname(os.path.realpath(__file__)), "faiss_index")

# Utility functions
def get_pdf_text(pdf_docs):
    return "".join(page.page_content for page in pdf_docs)

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(FAISS_INDEX_NAME)

def convert_pdfs_to_vectors(dir_path=PDF_DIRECTORY):
    if not os.path.isdir(dir_path):
        raise ValueError(f"The directory '{dir_path}' does not exist.")
    all_text_chunks = [] 
    for file_name in os.listdir(dir_path):
        if file_name.endswith(".pdf"):
            file_path = os.path.join(dir_path, file_name)
            print(f"Processing {file_name}...")
            loader = PyPDFLoader(file_path)
            documents = loader.load()
            text_chunks = get_text_chunks(get_pdf_text(documents))
            all_text_chunks.extend(text_chunks) 
    print("Vectorizing combined text chunks...")
    get_vector_store(all_text_chunks)
    print("Data vectorized successfully.")


def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, 
    Context:\n {context}?\n
    Question: \n{question}\n
    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-8b", temperature=0.3)
    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

# Query FAISS Index
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    faiss_index_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), FAISS_INDEX_NAME)

    if not os.path.exists(faiss_index_path):
        raise FileNotFoundError(f"FAISS index not found at {faiss_index_path}. Run the vector conversion first.")

    new_db = FAISS.load_local(faiss_index_path, embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    return response

# Example usage
if __name__ == "__main__":
    try:
        convert_pdfs_to_vectors()
    except Exception as e:
        print(f"Error: {str(e)}")
