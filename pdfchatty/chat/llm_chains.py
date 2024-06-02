from .prompt_templates import pdf_chat_prompt
from langchain.chains import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Chroma
from .utils import load_config
import chromadb

config = load_config()


def create_llm(model_path=config["ctransformers"]["model_path"]["large"],
               model_type=config["ctransformers"]["model_type"], model_config=config["ctransformers"]["model_config"]):
    return CTransformers(model=model_path, model_type=model_type, config=model_config)


def create_embeddings(embeddings_path=config["embeddings_path"]):
    return HuggingFaceInstructEmbeddings(model_name=embeddings_path)


def load_vectordb(embeddings):
    persistent_client = chromadb.PersistentClient(config["chromadb"]["chromadb_path"])
    return Chroma(
        client=persistent_client,
        collection_name=config["chromadb"]["collection_name"],
        embedding_function=embeddings,
    )


def load_pdf_chat_chain():
    return pdfChatChain()


class pdfChatChain:
    def __init__(self):
        vector_db = load_vectordb(create_embeddings())
        llm = create_llm()
        self.retriever = vector_db.as_retriever(
            search_kwargs={"k": config["chat_config"]["number_of_retrieved_documents"]})
        self.prompt = PromptTemplate.from_template(pdf_chat_prompt)
        self.chain = LLMChain(llm=llm, prompt=self.prompt)

    def run(self, user_input):
        # Retrieve relevant documents
        documents = self.retriever.get_relevant_documents(user_input)
        if not documents:
            raise ValueError("Information not in the document base.")

        # Combine documents and chat history into a single input
        context = " ".join([doc.page_content for doc in documents])
        inputs = {
            "context": context,
            "human_input": user_input
        }
        # Run the chain
        llm_answer = self.chain.run(inputs)
        document_names = [doc.metadata["source"] for doc in documents]
        return llm_answer, document_names
