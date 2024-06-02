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
        'pdf_directory': settings.PDF_DIRECTORY,
    }

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

from django.templatetags.static import static

def get_avatar(sender_type):
    if sender_type == "human":
        return static('chat/images/user_image.png')
    else:
        return static('chat/images/bot_image.png')

def load_pdfs_from_directory(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_files.append(os.path.join(directory, filename))
    return pdf_files
