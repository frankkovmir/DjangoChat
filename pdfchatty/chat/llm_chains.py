from .prompt_templates import pdf_chat_prompt
from langchain.chains import LLMChain
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Chroma
from operator import itemgetter
from .utils import load_config
import chromadb

config = load_config()

def create_llm(model_path=config["ctransformers"]["model_path"]["large"], model_type=config["ctransformers"]["model_type"], model_config=config["ctransformers"]["model_config"]):
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
        self.retriever = vector_db.as_retriever(search_kwargs={"k": config["chat_config"]["number_of_retrieved_documents"]})
        self.prompt = PromptTemplate.from_template(pdf_chat_prompt)
        self.chain = LLMChain(llm=llm, prompt=self.prompt)

    def run(self, user_input, chat_history):
        # Retrieve relevant documents
        documents = self.retriever.invoke(user_input)
        # Combine documents and chat history into a single input
        context = " ".join([doc.page_content for doc in documents])
        inputs = {
            "history": chat_history,
            "context": context,
            "human_input": user_input
        }
        # Run the chain
        return self.chain.run(inputs)
