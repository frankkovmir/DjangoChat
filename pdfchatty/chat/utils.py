import json
from datetime import datetime
import yaml
from django.templatetags.static import static
from langchain.schema.messages import HumanMessage, AIMessage
from django.conf import settings
import os

def load_config():
    return {
        'ctransformers': settings.CTRANSFORMERS,
        'chat_config': settings.CHAT_CONFIG,
        'pdf_text_splitter': settings.PDF_TEXT_SPLITTER,
        'embeddings_path': settings.EMBEDDINGS_PATH,
        'chromadb': settings.CHROMADB,
        'chat_sessions_database_path': settings.CHAT_SESSIONS_DATABASE_PATH,
        'pdf_directory': settings.PDF_DIRECTORY,
    }

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_avatar(sender_type):
    if sender_type == "human":
        return static('chat/images/user_image.png')
    else:
        return static('chat/images/bot_image.png')

def save_chat_history_json(chat_history, file_path):
    with open(file_path, "w") as f:
        json_data = [message.dict() for message in chat_history]
        json.dump(json_data, f)

def load_chat_history_json(file_path):
    with open(file_path, "r") as f:
        json_data = json.load(f)
        messages = [HumanMessage(**message) if message["type"] == "human" else AIMessage(**message) for message in json_data]
        return messages

def load_pdfs_from_directory(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_files.append(os.path.join(directory, filename))
    return pdf_files
