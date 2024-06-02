from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from .llm_chains import load_vectordb, create_embeddings
from .utils import load_config
import pypdfium2

config = load_config()

def extract_text_from_pdf(pdf_path):
    pdf_file = pypdfium2.PdfDocument(pdf_path)
    return "\n".join(pdf_file.get_page(page_number).get_textpage().get_text_range() for page_number in range(len(pdf_file)))

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=config["pdf_text_splitter"]["chunk_size"],
                                              chunk_overlap=config["pdf_text_splitter"]["overlap"],
                                              separators=config["pdf_text_splitter"]["separators"])
    return splitter.split_text(text)

def get_document_chunks(text_list):
    documents = []
    for text in text_list:
        for chunk in get_text_chunks(text):
            documents.append(Document(page_content=chunk))
    return documents

def add_documents_to_db(pdf_paths):
    texts = [extract_text_from_pdf(pdf_path) for pdf_path in pdf_paths]
    documents = get_document_chunks(texts)
    vector_db = load_vectordb(create_embeddings())
    vector_db.add_documents(documents)
    print("Documents added to db.")
